from skimage.segmentation import relabel_sequential
import numpy as np
from skimage.util._map_array import ArrayMap
from skimage import measure
from scipy import spatial
from stardist.matching import matching      
from skimage.segmentation import relabel_sequential
from skimage.io import imread, imsave

from tqdm import tqdm
import xarray as xr


def match_labels(ys, iou_threshold=0):
    """
    Matches object ids in a list of label images based on a matching criterion.
    For i=0..len(ys)-1 consecutively matches ys[i+1] with ys[i],
    matching objects retain their id, non matched objects will be assigned a new id
    Example
    -------
    import numpy as np
    from stardist.data import test_image_nuclei_2d
    from stardist.matching import match_labels
    _y = test_image_nuclei_2d(return_mask=True)[1]
    labels = np.stack([_y, 2*np.roll(_y,10)], axis=0)
    labels_new = match_labels(labels)
    Parameters
    ----------
    ys : np.ndarray, tuple of np.ndarray
          list/array of integer labels (2D or 3D)
    """

    ys = np.asarray(ys)
    if not ys.ndim in (3, 4):
        raise ValueError('label image y should be 3 or 4 dimensional!')

    def _match_single(x, y):
        # y = relabel_sequential(y, offset=x.max()+1)[0]
        offset = max(x.max(), y.max()) + 1
        res = matching(x, y, report_matches=True, thresh=0)

        pairs = tuple(p for p, s in zip(res.matched_pairs, res.matched_scores) if s >= iou_threshold)
        map_dict = dict((i2, i1) for i1, i2 in pairs)

        y2 = np.zeros_like(y)
        y_labels = set(np.unique(y)) - {0}

        # labels that can be used for non-matched objects
        # label_reservoir = list(set(np.arange(1, len(y_labels)+1)) - set(map_dict.values()))
        for r in measure.regionprops(y):
            m = (y[r.slice] == r.label)
            if r.label in map_dict:
                y2[r.slice][m] = map_dict[r.label]
            else:
                y2[r.slice][m] = offset
                offset += 1

        return y2

    ys_new = ys.copy()

    for i in range(len(ys)-1):
        ys_new[i+1] = _match_single(ys_new[i], ys[i+1])

    return ys_new



if __name__ == '__main__':

    iou_threshold = snakemake.params['iou_threshold']
    stacked_image = np.stack([ imread(f) for f in sorted(snakemake.input['labels'])], axis=0)
    outfiles = sorted(snakemake.output['matched'])
    
    relabeled_iou = match_labels(stacked_image.astype(int), iou_threshold=iou_threshold)
    
    for i in range(relabeled_iou.shape[0]):
        imsave(outfiles[i], relabeled_iou[i])