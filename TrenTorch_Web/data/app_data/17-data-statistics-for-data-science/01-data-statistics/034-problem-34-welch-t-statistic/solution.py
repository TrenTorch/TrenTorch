import numpy as np

def solve(a, b):
    """Implement welch t statistic according to the contract."""
    a, b = (np.asarray(a, float), np.asarray(b, float))
    va, vb = (np.var(a, ddof=1), np.var(b, ddof=1))
    return float((a.mean() - b.mean()) / np.sqrt(va / len(a) + vb / len(b)))
