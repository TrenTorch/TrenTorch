import numpy as np

def solve(X):
    X = np.asarray(X, dtype=float)
    return np.corrcoef(X, rowvar=False)
