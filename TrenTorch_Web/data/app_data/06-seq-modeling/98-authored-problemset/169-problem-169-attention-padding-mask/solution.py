import numpy as np

def solve(ids, pad_id):
    """Return a boolean attention mask that is False only at padding tokens."""
    return np.asarray(ids) != pad_id
