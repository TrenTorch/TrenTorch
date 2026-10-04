import numpy as np

def solve(x):
    """Implement median imputation according to the contract."""
    x = np.asarray(x, float).copy()
    m = np.nanmedian(x)
    x[np.isnan(x)] = m
    return x
