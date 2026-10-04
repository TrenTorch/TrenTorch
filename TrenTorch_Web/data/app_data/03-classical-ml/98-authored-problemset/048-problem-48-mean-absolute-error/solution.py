import numpy as np

def solve(y, pred):
    """Implement mean absolute error according to the contract."""
    return float(np.mean(np.abs(np.asarray(y, float) - np.asarray(pred, float))))
