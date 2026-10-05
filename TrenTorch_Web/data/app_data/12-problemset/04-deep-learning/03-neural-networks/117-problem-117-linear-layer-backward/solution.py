import numpy as np

def solve(X, dY, W):
    X = np.asarray(X)
    dY = np.asarray(dY)
    W = np.asarray(W)
    return dY @ W.T, X.T @ dY, dY.sum(axis=0)
