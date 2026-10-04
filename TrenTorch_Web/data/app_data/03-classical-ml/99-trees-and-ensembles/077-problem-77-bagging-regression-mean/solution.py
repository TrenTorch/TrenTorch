import numpy as np

def solve(predictions):
    """Implement bagging regression mean according to the contract."""
    return np.asarray(predictions, float).mean(0)
