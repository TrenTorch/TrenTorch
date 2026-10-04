import numpy as np

def solve(p1, p2):
    """Implement sample size for proportion according to the contract."""
    z1, z2 = (1.96, 0.84)
    p = (p1 + p2) / 2
    return int(np.ceil(2 * (z1 * np.sqrt(2 * p * (1 - p)) + z2 * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p1 - p2) ** 2))
