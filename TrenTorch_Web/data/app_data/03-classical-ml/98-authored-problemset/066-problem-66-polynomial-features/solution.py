import numpy as np

def solve(x, degree):
    """Implement polynomial features according to the contract."""
    x = np.asarray(x, float)
    return np.column_stack([x ** d for d in range(1, degree + 1)])
