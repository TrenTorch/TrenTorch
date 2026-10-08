import numpy as np


def bilinear_score(c, W, z):
    return float(np.asarray(c, dtype=float) @ np.asarray(W, dtype=float) @ np.asarray(z, dtype=float))
