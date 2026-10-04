import numpy as np

def solve(A, x):
    """Implement matrix-vector product according to the contract."""
    A, x = (np.asarray(A, float), np.asarray(x, float))
    return np.array([row @ x for row in A])
