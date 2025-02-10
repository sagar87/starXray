# Python program to demonstrate
# HDF5 file
 
import numpy as np
import zarr
import numpy as np
import xarray as xr
import h5py

if __name__ == "__main__":
    data = xr.open_zarr(snakemake.input['zarr'])
    
    # data.to_zarr(snakemake.output['zarr'])
 
# creating a file
    with h5py.File(snakemake.output['hdf5'], 'w') as f: 
        dset = f.create_dataset("image", data = data.image.values)
        dset = f.create_dataset("segmentation", data = data.filtered.values)