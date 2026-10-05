import numpy as np

def solve(x):
    x = np.asarray(x, dtype=float)
    shifted = x - np.max(x)
    exp_values = np.exp(shifted)
    return exp_values / exp_values.sum()
