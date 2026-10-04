import numpy as np

def solve(x):
    """Implement softmax vector according to the contract."""
    x = np.asarray(x, float)
    z = x - x.max(axis=-1, keepdims=True)
    p = np.exp(z)
    return p / p.sum(axis=-1, keepdims=True)
