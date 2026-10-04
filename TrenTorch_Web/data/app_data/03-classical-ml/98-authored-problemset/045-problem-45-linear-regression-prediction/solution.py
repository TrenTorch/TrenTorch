import numpy as np

def solve(X, w, b):
    """Implement linear regression prediction according to the contract."""
    return np.asarray(X) @ np.asarray(w) + b
