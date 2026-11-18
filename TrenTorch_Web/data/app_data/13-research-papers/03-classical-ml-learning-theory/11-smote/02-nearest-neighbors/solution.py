import numpy as np


def nearest_neighbors(X, x, k):
    d = np.linalg.norm(np.asarray(X, dtype=float) - np.asarray(x, dtype=float), axis=1)
    return np.argsort(d, kind="stable")[:k]
