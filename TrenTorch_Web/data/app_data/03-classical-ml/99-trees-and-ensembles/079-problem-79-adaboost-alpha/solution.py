import numpy as np

def solve(error):
    """Implement adaboost alpha according to the contract."""
    e = float(error)
    return 0.5 * np.log((1 - e) / e)
