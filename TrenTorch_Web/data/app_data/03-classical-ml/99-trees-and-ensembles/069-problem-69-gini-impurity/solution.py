import numpy as np

def solve(counts):
    """Implement gini impurity according to the contract."""
    c = np.asarray(counts, float)
    p = c / c.sum() if c.sum() else c
    return float(1 - np.sum(p * p))
