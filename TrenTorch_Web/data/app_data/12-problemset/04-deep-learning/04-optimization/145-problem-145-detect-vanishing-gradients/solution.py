import numpy as np

def solve(grad, threshold):
    """A gradient is vanishing when its Euclidean norm is strictly less than the supplied threshold."""
    return float(np.linalg.norm(np.asarray(grad)))<threshold
