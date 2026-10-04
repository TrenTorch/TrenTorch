import numpy as np

def solve(y, pred):
    """Implement confusion matrix according to the contract."""
    y, p = (np.asarray(y), np.asarray(pred))
    return np.array([[np.sum((y == 0) & (p == 0)), np.sum((y == 0) & (p == 1))], [np.sum((y == 1) & (p == 0)), np.sum((y == 1) & (p == 1))]])
