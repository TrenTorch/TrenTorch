import numpy as np

def solve(X, W, b):
    return np.asarray(X) @ np.asarray(W) + np.asarray(b)
