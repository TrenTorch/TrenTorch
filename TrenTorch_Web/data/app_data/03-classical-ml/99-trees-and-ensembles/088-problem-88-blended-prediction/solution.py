import numpy as np

def solve(predictions, weights):
    """Implement blended prediction according to the contract."""
    P, w = (np.asarray(predictions, float), np.asarray(weights, float))
    return w / w.sum() @ P
