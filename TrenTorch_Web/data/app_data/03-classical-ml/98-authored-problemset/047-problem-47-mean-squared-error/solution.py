import numpy as np

def solve(y, pred):
    """Implement mean squared error according to the contract."""
    return float(np.mean((np.asarray(y, float) - np.asarray(pred, float)) ** 2))
