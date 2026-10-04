import numpy as np

def solve(x):
    """Implement bernoulli mean and variance according to the contract."""
    x = np.asarray(x, float)
    p = float(np.mean(x))
    return (p, p * (1 - p))
