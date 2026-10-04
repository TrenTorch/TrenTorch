import numpy as np

def solve(y, pred):
    """Implement mse loss according to the contract."""
    return float(np.mean((np.asarray(y) - np.asarray(pred)) ** 2))
