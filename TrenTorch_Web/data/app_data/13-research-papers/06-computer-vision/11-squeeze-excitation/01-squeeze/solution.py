import numpy as np


def squeeze(x):
    return np.asarray(x, dtype=float).mean(axis=(0, 1))
