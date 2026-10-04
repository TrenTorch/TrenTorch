import numpy as np

def solve(pred, weak_pred, learning_rate):
    """Implement gradient boosting update according to the contract."""
    return np.asarray(pred, float) + learning_rate * np.asarray(weak_pred, float)
