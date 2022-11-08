# TEWA WS 22/23 – Individual Assignments

The goal of the individual assignment is to first preprocess a single subject’s data and afterwards perform a simple first-level analysis.

We will use the "NYU Slow Flanker" dataset from Openneuro. In this study, 26 healthy adults underwent MRI scanning while performing an event-related Eriksen Flanker task.

The preprocessing will be guided. That is, we will provide you with a Jupyter notebook (*individual-project-scaffold.ipynb*), which contains the setup of the necessary libraries (e.g., FSL) as well as the download of the sample dataset. Furthermore, we will add instructions regarding the specific preprocessing steps that should be included in your pipeline. The steps will be:

- Setting up a directory structure and define experiment variables 
- Define **preprocessing** steps (using Nipype Nodes), specifically:
	- Removing the first 4 volumes
	- Slicetime correction
	- Realignment (Motion Correction)
	- Coregistration of anatomical and functional image (using a pre-defined sub-workflow)
	- Normalization to the MNI template (using a pre-defined sub-workflow)
	- Smoothing
- Perform **sanity checks** on the output 
	- Plot output files
	- Inspect motion parameters and detected artefacts
- Perform **first-level analysis** on the preprocessed data (using Nilearn)

Both the preprocessing and the first-level analysis will be rather simple (compared to more elaborate pipelines), conforming to the limitations of the Google Colab environment. Also, due to their complexity some of the preprocessing steps will be predefined in the notebook. 

Please hand-in a notebook (.ipynb file) containing the whole procedure. Also, add some explanations by using text fields. 

You will find additional information in the notebook.
