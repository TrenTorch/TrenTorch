import numpy as np

def solve(p):
    p = np.asarray(p, dtype=float)
    if p.ndim != 1 or p.size == 0 or np.any(p < 0) or not np.isclose(p.sum(), 1.0):
        raise ValueError("p must be a non-empty 1-D probability vector that sums to 1")
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))
