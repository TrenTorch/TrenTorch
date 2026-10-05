import numpy as np


def row_norms(v):
    v = np.asarray(v, dtype=float)
    return np.sqrt(np.sum(v**2, axis=1))
