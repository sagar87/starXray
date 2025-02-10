import xarray as xr
from skimage.io import imread
import zarr
import numpy as np



if __name__ == "__main__":
    img = np.stack([imread(f) for f in sorted(snakemake.input['image'])], axis=0)
    seg = np.stack([imread(f) for f in sorted(snakemake.input['segmentation'])], axis=0)
    mat = np.stack([imread(f) for f in sorted(snakemake.input['matched'])], axis=0)
    mat = np.stack([imread(f) for f in sorted(snakemake.input['filtered'])], axis=0)
    
                   
    data = xr.Dataset({
        "image": xr.DataArray(img, dims=['z', 'y', 'x']),
        "segmentation": xr.DataArray(seg, dims=['z', 'y', 'x']),    
        "matched": xr.DataArray(mat, dims=['z', 'y', 'x']),    
        "filtered": xr.DataArray(mat, dims=['z', 'y', 'x']),    
    })
    
    data.to_zarr(snakemake.output['zarr'])