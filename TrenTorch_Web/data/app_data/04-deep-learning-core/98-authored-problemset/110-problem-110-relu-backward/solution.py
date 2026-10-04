import numpy as np

def solve(x):
    """Implement relu backward according to the contract."""
    return (np.asarray(x) > 0).astype(float)
