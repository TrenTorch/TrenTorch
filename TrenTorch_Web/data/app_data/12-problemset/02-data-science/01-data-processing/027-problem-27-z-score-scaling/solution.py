import numpy as np

def solve(X):
    X = np.asarray(X, dtype=float)
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    return np.divide(X - mean, std, out=np.zeros_like(X), where=std != 0)
