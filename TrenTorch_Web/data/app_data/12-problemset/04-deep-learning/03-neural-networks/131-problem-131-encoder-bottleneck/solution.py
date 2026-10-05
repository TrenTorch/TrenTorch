import numpy as np

def solve(X, W, b):
    """A linear encoder bottleneck maps each input row to a lower-dimensional representation using XW+b."""
    return np.asarray(X)@np.asarray(W)+np.asarray(b)
