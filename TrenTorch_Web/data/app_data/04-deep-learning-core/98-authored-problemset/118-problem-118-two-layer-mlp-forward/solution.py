import numpy as np

def solve(X, W1, b1, W2, b2):
    """Implement two-layer mlp forward according to the contract."""
    X, W1, b1, W2, b2 = map(np.asarray, (X, W1, b1, W2, b2))
    z1 = X @ W1 + b1
    h = np.maximum(z1, 0)
    return (h @ W2 + b2, (z1, h))
