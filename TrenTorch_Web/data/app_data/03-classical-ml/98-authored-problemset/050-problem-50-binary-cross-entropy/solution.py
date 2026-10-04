import numpy as np

def solve(y, p):
    """Implement binary cross-entropy according to the contract."""
    y, p = (np.asarray(y, float), np.asarray(p, float))
    p = np.clip(p, 1e-15, 1 - 1e-15)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
