import numpy as np

def solve(n):
    """Implement causal mask according to the contract."""
    i = np.arange(n)[:, None]
    j = np.arange(n)[None, :]
    return i >= j
