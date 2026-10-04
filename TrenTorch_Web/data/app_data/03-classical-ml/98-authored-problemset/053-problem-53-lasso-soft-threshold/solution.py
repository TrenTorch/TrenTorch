import numpy as np

def solve(z, lam):
    z = float(z)
    return float(np.sign(z) * max(abs(z) - lam, 0.0))
