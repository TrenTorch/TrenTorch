import numpy as np

def solve(x):
    x = np.asarray(x, dtype=float)
    exp_negative_abs = np.exp(-np.abs(x))
    return np.where(x >= 0, 1.0 / (1.0 + exp_negative_abs), exp_negative_abs / (1.0 + exp_negative_abs))
