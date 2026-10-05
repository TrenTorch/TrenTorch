import numpy as np

def solve(grad, threshold):
    """A gradient is exploding when its Euclidean norm is strictly greater than the supplied threshold."""
    return float(np.linalg.norm(np.asarray(grad)))>threshold
