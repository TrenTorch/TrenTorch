import numpy as np

def solve(n):
    return np.tril(np.ones((n, n), dtype=bool))
