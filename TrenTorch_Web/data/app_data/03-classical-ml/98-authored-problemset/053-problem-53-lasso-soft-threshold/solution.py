import numpy as np

def solve(z, lam):
    """Implement lasso soft threshold according to the contract."""
    z = float(z)
    return np.sign(z) * max(abs(z) - lam, 0.0)
