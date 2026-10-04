import numpy as np

def solve(ids, pad_id):
    """Implement sequence mask according to the contract."""
    return (np.asarray(ids) != pad_id).astype(int)
