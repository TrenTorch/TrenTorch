import numpy as np

def solve(x):
    """Implement relu activation according to the contract."""
    return np.maximum(np.asarray(x), 0)
