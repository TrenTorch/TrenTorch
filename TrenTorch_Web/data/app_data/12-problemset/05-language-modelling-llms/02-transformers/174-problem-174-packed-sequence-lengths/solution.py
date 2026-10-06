import numpy as np

def solve(lengths):
        return np.cumsum(np.r_[0,lengths[:-1]])
