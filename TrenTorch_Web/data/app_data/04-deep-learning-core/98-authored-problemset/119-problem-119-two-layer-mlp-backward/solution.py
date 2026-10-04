import numpy as np

def solve(X, dY, W1, W2, cache):
    """Implement two-layer mlp backward according to the contract."""
    X, dY, W1, W2 = map(np.asarray, (X, dY, W1, W2))
    z1, h = map(np.asarray, cache)
    dW2 = h.T @ dY
    db2 = dY.sum(0)
    dh = dY @ W2.T
    dz = dh * (z1 > 0)
    return (dz @ W1.T, X.T @ dz, dz.sum(0), dW2, db2)
