import numpy as np

def solve(n, k):
    idx = np.arange(n)
    return [(np.setdiff1d(idx, valid), valid) for valid in np.array_split(idx, k)]
