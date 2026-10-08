import math

import numpy as np


def magnitude_mask(w, keep_fraction):
    flat = np.abs(np.asarray(w, dtype=float).ravel())
    k = math.ceil(keep_fraction * flat.size)
    mask = np.zeros(flat.size, dtype=bool)
    if k > 0:
        mask[np.argsort(-flat, kind="stable")[:k]] = True
    return mask.reshape(np.shape(w))
