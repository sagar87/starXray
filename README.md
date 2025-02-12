# starXray 

*A pipeline for automated 3D instance segmentation of blob-like structures in X-ray image data.*

This GitHub repository provides a pipeline for automating the 3D segmentation of blob-like structures in X-ray image data.

The workflow consists of two main steps:

1. A Snakemake pipeline that applies StarDist (2D) to each z-stack of the X-ray dataset, aligns the segmentations, and generates an initial 3D instance segmentation.
2. A Jupyter Notebook that utilizes the initial segmentation to train a StarDist3D model, enabling direct application to the dataset.

![pipeline](https://github.com/sagar87/starXray/blob/main/img/pipeline.png?raw=true)
