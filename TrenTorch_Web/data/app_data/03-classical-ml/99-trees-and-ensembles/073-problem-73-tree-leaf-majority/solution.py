import numpy as np

def solve(y):
    """Implement tree leaf majority according to the contract."""
    u, c = np.unique(y, return_counts=True)
    return u[np.argmax(c)]
