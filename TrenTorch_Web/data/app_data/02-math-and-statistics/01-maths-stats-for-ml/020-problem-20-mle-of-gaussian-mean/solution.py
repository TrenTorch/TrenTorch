import numpy as np

def solve(x):
    """Implement mle of gaussian mean according to the contract."""
    return float(np.mean(np.asarray(x, float)))
