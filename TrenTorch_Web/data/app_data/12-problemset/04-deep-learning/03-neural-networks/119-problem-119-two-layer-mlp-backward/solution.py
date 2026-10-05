import numpy as np

def solve(X, dY, W1, W2, cache):
    X = np.asarray(X)
    dY = np.asarray(dY)
    W1 = np.asarray(W1)
    W2 = np.asarray(W2)
    z1, h = cache
    z1 = np.asarray(z1)
    h = np.asarray(h)
    dW2 = h.T @ dY
    db2 = dY.sum(axis=0)
    dz1 = (dY @ W2.T) * (z1 > 0)
    dX = dz1 @ W1.T
    dW1 = X.T @ dz1
    db1 = dz1.sum(axis=0)
    return dX, dW1, db1, dW2, db2
