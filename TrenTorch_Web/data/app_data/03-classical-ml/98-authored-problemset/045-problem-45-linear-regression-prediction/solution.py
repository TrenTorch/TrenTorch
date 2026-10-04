import numpy as np

def solve(X, w, b):
    return np.asarray(X, dtype=float) @ np.asarray(w, dtype=float) + b
