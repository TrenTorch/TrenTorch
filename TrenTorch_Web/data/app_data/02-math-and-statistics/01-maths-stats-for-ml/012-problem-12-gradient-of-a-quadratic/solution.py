import numpy as np

def solve(A, x, b):
    """Implement gradient of a quadratic according to the contract."""
    A, x, b = (np.asarray(A, float), np.asarray(x, float), np.asarray(b, float))
    return 0.5 * (A + A.T) @ x + b
