import numpy as np

def solve(y, h, weights, error):
    """Implement adaboost weight update according to the contract."""
    y = np.asarray(y)
    h = np.asarray(h)
    w = np.asarray(weights, float)
    alpha = 0.5 * np.log((1 - error) / max(error, 1e-15))
    w *= np.exp(-alpha * y * h)
    return w / w.sum()
