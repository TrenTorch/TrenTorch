import numpy as np

def solve(X, C):
    """Implement k-means assignment according to the contract."""
    X = np.asarray(X, float)
    C = np.asarray(C, float)
    return np.argmin(((X[:, None, :] - C[None, :, :]) ** 2).sum(2), axis=1)
