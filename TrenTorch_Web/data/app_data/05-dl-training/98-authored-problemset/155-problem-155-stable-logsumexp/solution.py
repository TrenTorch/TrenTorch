import numpy as np

def solve(x):
    """Implement stable logsumexp according to the contract."""
    x = np.asarray(x, float)
    m = np.max(x)
    return float(m + np.log(np.sum(np.exp(x - m))))
