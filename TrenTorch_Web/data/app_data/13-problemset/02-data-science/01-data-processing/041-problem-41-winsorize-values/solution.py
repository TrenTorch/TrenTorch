import numpy as np

def solve(x, lower=0.05, upper=0.95):
    x = np.asarray(x, dtype=float)
    low, high = np.quantile(x, [lower, upper])
    return np.clip(x, low, high)
