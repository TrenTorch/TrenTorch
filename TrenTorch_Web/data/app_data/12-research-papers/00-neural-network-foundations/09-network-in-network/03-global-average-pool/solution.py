import numpy as np


def global_average_pool(x):
    return np.asarray(x, dtype=float).mean(axis=(0, 1))
