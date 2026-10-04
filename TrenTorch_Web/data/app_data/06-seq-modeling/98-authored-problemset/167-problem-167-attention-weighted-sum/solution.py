import numpy as np

def solve(weights, V):
    """Implement attention weighted sum according to the contract."""
    return np.asarray(weights) @ np.asarray(V)
