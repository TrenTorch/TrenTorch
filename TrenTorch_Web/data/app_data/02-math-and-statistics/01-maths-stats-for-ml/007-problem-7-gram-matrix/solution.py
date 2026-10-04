import numpy as np

def solve(X):
    X = np.asarray(X, dtype=float)
    return X.T @ X
