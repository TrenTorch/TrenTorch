import numpy as np

def solve(x):
    """Implement mean imputation according to the contract."""
    x = np.asarray(x, float).copy()
    m = np.nanmean(x)
    x[np.isnan(x)] = m
    return x
