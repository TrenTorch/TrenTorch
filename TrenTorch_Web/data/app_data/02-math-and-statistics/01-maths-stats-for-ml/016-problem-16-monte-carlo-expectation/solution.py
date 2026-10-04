import numpy as np

def solve(f, samples):
    """Implement monte carlo expectation according to the contract."""
    return float(np.mean(f(np.asarray(samples))))
