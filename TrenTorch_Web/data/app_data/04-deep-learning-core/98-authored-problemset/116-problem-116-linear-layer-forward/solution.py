import numpy as np

def solve(X, W, b):
    """Implement linear layer forward according to the contract."""
    return np.asarray(X) @ np.asarray(W) + np.asarray(b)
