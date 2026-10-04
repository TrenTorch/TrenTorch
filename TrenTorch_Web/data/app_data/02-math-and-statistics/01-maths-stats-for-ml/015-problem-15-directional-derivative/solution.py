import numpy as np

def solve(grad, direction):
    """Implement directional derivative according to the contract."""
    d = np.asarray(direction, float)
    d = d / np.linalg.norm(d)
    return float(grad @ d)
