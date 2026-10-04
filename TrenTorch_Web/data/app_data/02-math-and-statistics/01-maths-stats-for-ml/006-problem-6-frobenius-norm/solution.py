import numpy as np

def solve(x):
    """Implement frobenius norm according to the contract."""
    x = np.asarray(x, float)
    return float(np.sqrt(np.sum(x * x)))
