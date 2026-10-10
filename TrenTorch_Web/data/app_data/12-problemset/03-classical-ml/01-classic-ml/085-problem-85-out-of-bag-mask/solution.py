import numpy as np

def solve(n, bootstrap_indices):
    mask = np.ones(n, dtype=bool)
    mask[np.asarray(bootstrap_indices, dtype=int)] = False
    return mask
