import xarray as xr
from skimage.io import imread
import zarr
import numpy as np
from skimage.measure import regionprops_table
import pandas as pd



if __name__ == "__main__":
    img = imread(snakemake.input['image'])
    seg = imread(snakemake.input['segmentation'])
    
    df = pd.DataFrame(
        regionprops_table(
            seg.astype(int), 
            intensity_image=img,
            properties=('label', 'area', 'area_bbox', 'axis_major_length','axis_minor_length','centroid', 'intensity_max', 'intensity_mean')
    )).assign(image=snakemake.input['image'])
    
    df.to_csv(snakemake.output['props'])