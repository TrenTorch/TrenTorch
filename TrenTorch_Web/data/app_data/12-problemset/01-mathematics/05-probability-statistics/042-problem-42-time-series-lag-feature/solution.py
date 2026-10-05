import numpy as np

def solve(x):
    x = np.asarray(x, dtype=float)
    result = np.empty(len(x), dtype=float)
    result[0] = np.nan
    result[1:] = x[:-1]
    return result
