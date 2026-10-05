import numpy as np

def solve(X, W1, b1, W2, b2):
    X = np.asarray(X)
    W1 = np.asarray(W1)
    W2 = np.asarray(W2)
    z1 = X @ W1 + np.asarray(b1)
    h = np.maximum(z1, 0)
    output = h @ W2 + np.asarray(b2)
    return output, (z1, h)
