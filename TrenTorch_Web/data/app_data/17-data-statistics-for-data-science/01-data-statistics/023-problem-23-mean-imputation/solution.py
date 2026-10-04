import numpy as np

def solve(x):
    x = np.asarray(x, dtype=float).copy()
    mean = np.nanmean(x)
    x[np.isnan(x)] = mean
    return x
