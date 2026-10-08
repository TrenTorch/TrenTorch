import numpy as np


def clip_by_norm(g, threshold):
    g = np.asarray(g, dtype=float)
    n = np.linalg.norm(g)
    return g if n <= threshold else g * (threshold / n)
