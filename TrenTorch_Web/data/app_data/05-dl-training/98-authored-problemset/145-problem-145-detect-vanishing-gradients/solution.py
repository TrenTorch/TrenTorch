import numpy as np

def solve(grad, threshold):
    """Implement detect vanishing gradients according to the contract."""
    n = float(np.linalg.norm(np.asarray(grad)))
    return n < threshold
