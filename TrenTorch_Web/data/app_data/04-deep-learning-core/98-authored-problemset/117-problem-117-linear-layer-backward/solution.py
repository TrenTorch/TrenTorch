import numpy as np

def solve(X, dY, W):
    """Implement linear layer backward according to the contract."""
    X, dY, W = (np.asarray(X), np.asarray(dY), np.asarray(W))
    return (dY @ W.T, X.T @ dY, dY.sum(0))
