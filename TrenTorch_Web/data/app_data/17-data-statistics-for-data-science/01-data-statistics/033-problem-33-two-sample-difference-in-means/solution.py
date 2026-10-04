import numpy as np

def solve(a, b):
    """Implement two-sample difference in means according to the contract."""
    return float(np.mean(a) - np.mean(b))
