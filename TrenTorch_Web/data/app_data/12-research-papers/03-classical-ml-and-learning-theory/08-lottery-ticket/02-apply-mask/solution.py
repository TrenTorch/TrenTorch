import numpy as np


def apply_mask(w, mask):
    return np.asarray(w, dtype=float) * np.asarray(mask)
