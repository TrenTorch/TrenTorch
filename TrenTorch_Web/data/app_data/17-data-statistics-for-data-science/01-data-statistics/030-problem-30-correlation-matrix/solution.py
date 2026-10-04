import numpy as np

def solve(x):
    """Implement correlation matrix according to the contract."""
    X = np.asarray(x, float)
    Z = (X - X.mean(0)) / X.std(0)
    return Z.T @ Z / (len(X) - 1)
