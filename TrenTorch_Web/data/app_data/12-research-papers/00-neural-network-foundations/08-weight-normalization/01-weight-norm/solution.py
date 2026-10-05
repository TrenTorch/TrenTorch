import numpy as np


def weight_norm(v, g):
    v = np.asarray(v, dtype=float)
    norms = np.sqrt(np.sum(v**2, axis=1, keepdims=True))
    return g[:, None] * v / norms
