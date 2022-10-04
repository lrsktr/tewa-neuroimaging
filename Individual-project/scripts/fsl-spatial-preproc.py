import os 
from nipype import Workflow, Node
from nipype.interfaces.fsl import BET, FAST, Threshold, FLIRT, FNIRT, ApplyWarp
from nipype.interfaces.fsl.utils import RobustFOV




# Helper function to select WM segmentation file from segmentation output
def get_wm(files):
    return files[-1]


def create_fsl_coregflow(base_directory, apply_to_epis=False):

    ''' Creates FSL like coregistration worfklow

    Returns: Nipype Workflow object
    
    '''

    coreg_wf = Workflow(name='coreg_wf', base_dir=base_directory)

    # Remove neck from anatomical image to improve skullstripping
    strip_neck = Node(RobustFOV(),
                        name="strip_neck")

    # Skullstrip anatomical Image
    bet_anat = Node(BET(frac=0.2,
                            #reduce_bias=True,
                            output_type='NIFTI_GZ'),
                    name="bet_anat")

    # T1 segmentation & bias field correction
    segmentation = Node(FAST(output_type='NIFTI_GZ', output_biascorrected=True),
                        name="segmentation", mem_gb=4)

    # Threshold WM probability image
    threshold = Node(Threshold(thresh=0.15,
                            args='-bin',
                            output_type='NIFTI_GZ'),
                    name="threshold")

    # Pre-alignment of functional images to anatomical images
    coreg_pre = Node(FLIRT(dof=6, output_type='NIFTI_GZ'),
                    name="coreg_pre")

    # Use BBR cost function to improve the coregistration
    coreg_bbr = Node(FLIRT(dof=6,
                        cost='bbr',
                        schedule=os.path.join(os.getenv('FSLDIR'),"etc/flirtsch/bbr.sch"),      
                        output_type='NIFTI_GZ'),
                    name="coreg_bbr")

    # Apply coregistration warp to functional images
    applywarp = Node(FLIRT(interp='spline',
                        apply_isoxfm=4,
                        output_type='NIFTI'),
                    name="applywarp")


    # connect nodes of coreg workflow
    coreg_wf.connect([  (strip_neck, bet_anat,      [("out_roi", "in_file")]),
                        (bet_anat, segmentation,    [('out_file', 'in_files')]),
                        (segmentation, threshold,   [(('partial_volume_files', get_wm),
                                                       'in_file')]),
                        (bet_anat, coreg_pre,       [('out_file', 'reference')]),
                        (threshold, coreg_bbr,      [('out_file', 'wm_seg')]),
                        (coreg_pre, coreg_bbr,      [('out_matrix_file', 'in_matrix_file')]),
                        (bet_anat, coreg_bbr,       [('out_file', 'reference')])
                        ])


    if apply_to_epis:
        coreg_wf.connect(coreg_bbr, "out_matrix_file", applywarp, "in_matrix_file")
        coreg_wf.connect(bet_anat, "out_file", applywarp, "reference")
        
    return coreg_wf


def create_fsl_normflow(base_directory, reference):
    
    ''' Creates FSL like normalization worfklow

    Returns: Nipype Workflow object
    
    '''

    norm_wf = Workflow(name='norm_wf', base_dir=base_directory)
    
    # linear transformation of t1 to mni template
    mnimat_lin  = Node(FLIRT(cost_func="normcorr", dof=12, reference=reference),
                       name="mnimat_lin")                                                    

    # non-linear transformation of t1 to mni (using params from linear transf.)                                                                                
    anat2mni    = Node(FNIRT(ref_file=reference, warped_file="warped.nii"),
                       name="anat2mni")                                                    
                                                                                    
    # warp epi data to mni template
    warp_to_mni = Node(ApplyWarp(ref_file=reference),
                    name="warp_to_mni") 

    norm_wf.connect( [   
                        (mnimat_lin, anat2mni,    [("out_matrix_file", "affine_file")]),
                        (anat2mni, warp_to_mni,   [("field_file", "field_file")]),
                        (mnimat_lin, warp_to_mni, [("out_matrix_file", "postmat")]),
    ])


    return norm_wf

