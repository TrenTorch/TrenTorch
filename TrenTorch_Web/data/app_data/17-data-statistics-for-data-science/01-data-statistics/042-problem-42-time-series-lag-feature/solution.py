import numpy as np

def solve(x):
    """Implement time-series lag feature according to the contract."""
    x = np.asarray(x)
    out = np.empty(len(x), dtype=float)
    out[0] = np.nan
    out[1:] = x[:-1]
    return out
