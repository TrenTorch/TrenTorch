import numpy as np

def solve(x, lower=0.05, upper=0.95):
    """Implement winsorize values according to the contract."""
    x = np.asarray(x, float)
    lo, hi = np.quantile(x, [lower, upper])
    return np.clip(x, lo, hi)
