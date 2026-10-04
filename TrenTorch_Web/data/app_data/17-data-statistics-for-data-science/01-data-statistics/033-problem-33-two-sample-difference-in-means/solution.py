import numpy as np

def solve(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.mean(a) - np.mean(b))
