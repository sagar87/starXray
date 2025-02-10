from pathlib import Path
import pandas as pd

# path to the volume
DATA = Path("data/volume")
PATH = Path("project")

SAMPLES = [ str(f).split('/')[-1].replace('.tif','') for f in DATA.glob("*.tif") ]

rule all:
    input: 
        expand(PATH / "labels/{sample}.tif", sample=SAMPLES),
        expand(PATH / "matched/{sample}.tif", sample=SAMPLES),
        PATH / "regionprops/regionprops_unmatched.csv",
        PATH / "regionprops/regionprops_matched.csv",
        directory(PATH / "zarr/results.zarr"),
        PATH / "hdf5/results.hdf5"

rule stardist:
    input:
        image = DATA / "{sample}.tif",
    output:
        labels = PATH / "labels/{sample}.tif",
    retries: 3
    conda:
        "/home/voehring/voehring/conda/stardist-new"
    script:
        "scripts/stardist.py"


rule match_segmentation:
    input:
        labels = expand(PATH / "labels/{sample}.tif", sample=SAMPLES)
    output:
        matched = expand(PATH / "matched/{sample}.tif", sample=SAMPLES)
    params:
        iou_threshold = 0.6
    resources:
        mem_mb=96000,
    conda:
        "/home/voehring/voehring/conda/stardist-new"
    script:
        "scripts/match_segmentation.py"


# Following rules can be skipped (this we just run for inspecting the data)
rule regionprops_unmatched:
    input:
        image = DATA / "{sample}.tif",
        segmentation = PATH / "labels/{sample}.tif"
    output:
        props = temp(PATH / "regionprops/{sample}_unmatched.csv")
    conda:
        "/home/voehring/voehring/conda/stardist-new"
    script:
        "scripts/regionprops.py"


rule concatenate_regionprops_unmatched:
    input:
        regionprops = expand(PATH / "regionprops/{sample}_unmatched.csv", sample=SAMPLES)
    output:
        concatenated = PATH / "regionprops/regionprops_unmatched.csv"
    resources:
        mem_mb=64000,        
    run:
        pd.concat([ pd.read_csv(df) for df in input.regionprops ]).to_csv(output.concatenated)

# more important are the matched ones
rule regionprops_matched:
    input:
        image = DATA / "{sample}.tif",
        segmentation = PATH / "matched/{sample}.tif"
    output:
        props = temp(PATH / "regionprops/{sample}_matched.csv")
    conda:
        "/home/voehring/voehring/conda/stardist-new"
    script:
        "scripts/regionprops.py"


rule concatenate_regionprops_matched:
    input:
        regionprops = expand(PATH / "regionprops/{sample}_matched.csv", sample=SAMPLES)
    output:
        concatenated = PATH / "regionprops/regionprops_matched.csv"
    resources:
        mem_mb=64000,        
    run:
        pd.concat([ pd.read_csv(df) for df in input.regionprops ]).to_csv(output.concatenated)


rule filter_segmentation:
    input:
        matched = expand(PATH / "matched/{sample}.tif", sample=SAMPLES),
        concatenated = PATH / "regionprops/regionprops_matched.csv"
    output:
        filtered = expand(PATH / "filtered/{sample}.tif", sample=SAMPLES)
    params:
        min_z = 5,
        max_volume = 10000
    resources:
        mem_mb=96000,
    conda:
        "/home/voehring/voehring/conda/stardist-new"
    script:
        "scripts/filter_segmentation.py"

# for export
rule zarr:
    input:
        image = expand(DATA / "{sample}.tif", sample=SAMPLES),
        segmentation = expand(PATH / "labels/{sample}.tif", sample=SAMPLES),
        matched = expand(PATH / "matched/{sample}.tif", sample=SAMPLES),
        filtered = expand(PATH / "filtered/{sample}.tif", sample=SAMPLES)
    output:
        zarr = directory(PATH / "zarr/results.zarr")
    resources:
        mem_mb=96000,
    conda:
        "/home/voehring/voehring/conda/stardist-new"
    script:
        "scripts/zarr.py"


rule hdf5:
    input:
        zarr = directory(PATH / "zarr/results.zarr")
    output:
        hdf5 = PATH / "hdf5/results.hdf5"
    resources:
        mem_mb=96000,
    conda:
        "/home/voehring/voehring/conda/stardist-new"
    script:
        "scripts/hdf.py"