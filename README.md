# starXray 

*A pipeline for automated 3D instance segmentation of blob-like structures in X-ray image data.*

![3D](https://github.com/sagar87/starXray/blob/main/img/3d_seg.png?raw=true)

This GitHub repository provides a pipeline for automating the 3D segmentation of blob-like structures in X-ray image data.

The workflow consists of two main steps:

1. A Snakemake pipeline that applies StarDist (2D) to each z-stack of the X-ray dataset, aligns the segmentations, and generates an initial 3D instance segmentation.
2. A Jupyter Notebook that utilizes the initial segmentation to train a StarDist3D model, enabling direct application to the dataset.

![pipeline](https://github.com/sagar87/starXray/blob/main/img/pipeline.png?raw=true)


## Running the Pipeline  

To run the pipeline, please familiarize yourself with the code and adapt it to your computing environment.  

### Setup Instructions:  

- The **Snakemake pipeline** is designed for use on **high-performance computing (HPC) systems**.  
- Use the **Conda environment file** (`envs/starxray.yaml`) to install all necessary dependencies. Some dependencies may require manual installation.  
- Update the **paths** and **Conda directives** in the Snakemake pipeline to match your system configuration.  


![output](https://github.com/sagar87/starXray/blob/main/img/output.png?raw=true)

