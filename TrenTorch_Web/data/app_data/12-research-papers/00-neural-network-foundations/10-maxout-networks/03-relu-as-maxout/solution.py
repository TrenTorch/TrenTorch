import numpy as np


def relu_via_maxout(x):
    x = np.asarray(x, dtype=float)
    pieces = np.stack([x, np.zeros_like(x)], axis=-1)
    return pieces.max(axis=-1)
