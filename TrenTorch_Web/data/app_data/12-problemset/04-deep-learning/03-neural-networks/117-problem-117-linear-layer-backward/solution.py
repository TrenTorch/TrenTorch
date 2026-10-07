import numpy as np

def solve(X, dY, W):
    X = np.asarray(X, dtype=float)
    dY = np.asarray(dY, dtype=float)
    W = np.asarray(W, dtype=float)
    return dY @ W.T, X.T @ dY, dY.sum(axis=0)
