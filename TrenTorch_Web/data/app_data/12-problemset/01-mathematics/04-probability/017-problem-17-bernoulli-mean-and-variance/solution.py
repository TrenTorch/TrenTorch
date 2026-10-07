import numpy as np

def solve(x):
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or x.size == 0 or not np.all((x == 0) | (x == 1)):
        raise ValueError("x must be a non-empty 1-D sequence of 0/1 values")
    p = float(np.mean(x))
    return p, p * (1 - p)
