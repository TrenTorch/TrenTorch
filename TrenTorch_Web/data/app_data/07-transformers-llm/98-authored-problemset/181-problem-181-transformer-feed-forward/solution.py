import numpy as np

def solve(x, W1, b1, W2, b2):
    """Apply a two-layer position-wise feed-forward network with ReLU."""
    hidden = np.maximum(0, np.asarray(x) @ W1 + b1)
    return hidden @ W2 + b2
