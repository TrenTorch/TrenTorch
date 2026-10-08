import numpy as np


def residual_distribution(p, q):
    r = np.maximum(np.asarray(p, dtype=float) - np.asarray(q, dtype=float), 0.0)
    return r / r.sum()
