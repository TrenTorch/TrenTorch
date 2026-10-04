import numpy as np

def solve(x, W1, b1, W2, b2):
    """Implement transformer feed-forward according to the contract."""
    return np.maximum(0, np.asarray(x) @ W1 + b1) @ W2 + b2
