import numpy as np

def solve(labels):
    """Implement in-context majority vote according to the contract."""
    u, c = np.unique(labels, return_counts=True)
    return u[np.argmax(c)]
