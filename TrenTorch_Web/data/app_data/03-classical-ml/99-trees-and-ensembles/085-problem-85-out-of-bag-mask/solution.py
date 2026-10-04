import numpy as np

def solve(sample_indices, n):
    """Implement out-of-bag mask according to the contract."""
    mask = np.ones(n, dtype=bool)
    mask[np.asarray(sample_indices, dtype=int)] = False
    return mask
