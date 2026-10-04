import numpy as np

def solve(x, sublayer):
    """Implement transformer residual block according to the contract."""
    return np.asarray(x) + sublayer(x)
