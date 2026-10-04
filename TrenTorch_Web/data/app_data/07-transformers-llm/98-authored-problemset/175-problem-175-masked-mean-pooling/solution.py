import numpy as np

def solve(E, mask):
    """Implement masked mean pooling according to the contract."""
    E, m = (np.asarray(E, float), np.asarray(mask, float)[:, :, None])
    return (E * m).sum(1) / np.maximum(m.sum(1), 1)
