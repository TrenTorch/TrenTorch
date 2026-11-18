import numpy as np


def upsample_nearest(x, f):
    x = np.asarray(x, dtype=float)
    return np.repeat(np.repeat(x, f, axis=0), f, axis=1)
