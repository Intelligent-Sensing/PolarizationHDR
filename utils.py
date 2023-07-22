import torch
import numpy as np


def uniform_weights(images, zmin, zmax):
    # return np.where((images >= zmin) & (images <= zmax), 1, 0)
    mask0 = np.where((images[..., 0] >= zmin) & (images[..., 0] <= zmax), 1, 0)
    mask1 = np.where((images[..., 1] >= zmin) & (images[..., 1] <= zmax), 1, 0)
    mask2 = np.where((images[..., 2] >= zmin) & (images[..., 2] <= zmax), 1, 0)
    # mask = np.where((mask0==1)&(mask1==1)&(mask2==1), 1, 0)
    mask = np.where((mask0 == 1) | (mask1 == 1) | (mask2 == 1), 1, 0)
    mask = np.repeat(mask[..., np.newaxis], 3, axis=2)

    return mask


def normalize(vector):
    if torch.is_tensor(vector):
        return (vector - torch.min(vector)) / (torch.max(vector) - torch.min(vector))
    else:
        return (vector - np.min(vector)) / (np.max(vector) - np.min(vector))
