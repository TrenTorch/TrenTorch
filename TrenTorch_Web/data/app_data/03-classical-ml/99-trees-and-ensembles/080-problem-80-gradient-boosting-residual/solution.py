import numpy as np

def solve(y, pred):
    """Implement gradient boosting residual according to the contract."""
    return np.asarray(y, float) - np.asarray(pred, float)
