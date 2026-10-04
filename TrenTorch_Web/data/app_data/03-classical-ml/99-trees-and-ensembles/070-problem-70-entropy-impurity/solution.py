import numpy as np

def solve(counts):
    """Implement entropy impurity according to the contract."""
    c = np.asarray(counts, float)
    p = c / c.sum() if c.sum() else c
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))
