import numpy as np

def solve(f, x, h=1e-05):
    """Implement finite difference derivative according to the contract."""
    return float((f(x + h) - f(x - h)) / (2 * h))
