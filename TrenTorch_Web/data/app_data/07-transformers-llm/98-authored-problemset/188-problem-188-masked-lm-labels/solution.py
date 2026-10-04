import numpy as np

def solve(ids, mask, ignore_index=-100):
    """Implement masked lm labels according to the contract."""
    ids = np.asarray(ids).copy()
    labels = np.full_like(ids, ignore_index)
    labels[mask] = ids[mask]
    return (ids, labels)
