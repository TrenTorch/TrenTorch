import numpy as np

def solve(x):
    """Implement gram matrix according to the contract."""
    X = np.asarray(x, float)
    return X.T @ X
