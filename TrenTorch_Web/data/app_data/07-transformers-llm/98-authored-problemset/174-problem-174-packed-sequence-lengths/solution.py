import numpy as np

def solve(lengths):
    """Implement packed sequence lengths according to the contract."""
    return np.cumsum(np.r_[0, lengths[:-1]])
