from skimage.segmentation import relabel_sequential
import numpy as np
from skimage.util._map_array import ArrayMap
from skimage import measure
from scipy import spatial
from stardist.matching import matching      
from skimage.segmentation import relabel_sequential
from skimage.io import imread, imsave
import pandas as pd
from tqdm import tqdm
import xarray as xr


if __name__ == '__main__':

    min_z = snakemake.params['min_z']
    max_volume = snakemake.params['max_volume']
    
    stacked_image = np.stack([ imread(f) for f in sorted(snakemake.input['matched'])], axis=0)
    
    props = (
        pd.read_csv(snakemake.input['concatenated'])
        .assign(z=lambda df: df['image'].apply(lambda x: int(x.split('_')[1].replace('.tif', ''))))
        .assign(z_height=1)
        .groupby('label')
        .agg({'z_height': 'sum', 'area': 'sum'})
        .rename(columns={'z_height': 'z', 'area': 'volume'})
        .reset_index()
    )
    
    white_list = props[(props.z > min_z) & (props.volume < max_volume)].label.tolist()
    filtered = np.where(np.isin(stacked_image, white_list), stacked_image, 0)
    
    outfiles = sorted(snakemake.output['filtered'])
    
    for i in range(filtered.shape[0]):
        imsave(outfiles[i], filtered[i])