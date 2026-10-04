import numpy as np

def solve(p):
    """Implement entropy of a distribution according to the contract."""
    p = np.asarray(p, float)
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))
