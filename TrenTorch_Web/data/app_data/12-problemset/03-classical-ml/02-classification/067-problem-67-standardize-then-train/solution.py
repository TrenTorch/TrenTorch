import numpy as np

def solve(x):
    x = np.asarray(x, dtype=float)
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    safe_std = np.where(std == 0, 1.0, std)
    return (x - mean) / safe_std
