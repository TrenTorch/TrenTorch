import numpy as np


def context_vector(weights, H):
    return np.asarray(weights, dtype=float) @ np.asarray(H, dtype=float)
