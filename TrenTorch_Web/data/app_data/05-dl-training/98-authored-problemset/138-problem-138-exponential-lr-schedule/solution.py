import numpy as np

def solve(lr0, gamma, t):
    """Implement exponential lr schedule according to the contract."""
    return lr0 * gamma ** t
