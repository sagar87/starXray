from stardist.models import StarDist2D

from stardist.data import test_image_nuclei_2d
from stardist.plot import render_label
from csbdeep.utils import normalize
import numpy as np

from glob import glob
import skimage.io as io


# prints a list of available models
StarDist2D.from_pretrained()

# creates a pretrained model
model = StarDist2D.from_pretrained('2D_versatile_fluo')

def get_labels(normed):
    labels, res = model.predict_instances(normed, scale=3)
    return labels, res

if __name__ == '__main__':
    img = io.imread(snakemake.input['image'])
    
    perc =  (img > 0).sum() / np.prod(img.shape) 
    
    if perc < 0.005:
        io.imsave(snakemake.output['labels'], np.zeros(img.shape)) 
        # not really needed for the rest of the pipeline
        # pickle.dump({}, open(snakemake.output['probs'], 'wb'))   
    else:
        normed = normalize(img)
        labels, probs = get_labels(normed)
        
        io.imsave(snakemake.output['labels'], labels)    
        # not really needed for the rest of the pipeline
        # pickle.dump(probs, open(snakemake.output['probs'], 'wb')) 
