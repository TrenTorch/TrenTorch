import numpy as np

def solve(counts):
    c = np.asarray(counts, dtype=float)
    if np.any(c < 0):
        raise ValueError("counts must be non-negative")
    total = c.sum()
    if total == 0:
        return 0.0
    p = c / total
    return float(1 - np.sum(p * p))
