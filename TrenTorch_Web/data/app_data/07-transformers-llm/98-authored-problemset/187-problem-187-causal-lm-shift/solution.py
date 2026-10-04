import numpy as np

def solve(ids):
    """Implement causal lm shift according to the contract."""
    ids = np.asarray(ids)
    return (ids[:-1], ids[1:])
