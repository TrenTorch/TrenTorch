import numpy as np

def solve(x):
    x = np.asarray(x, dtype=float).copy()
    median = np.nanmedian(x)
    x[np.isnan(x)] = median
    return x
