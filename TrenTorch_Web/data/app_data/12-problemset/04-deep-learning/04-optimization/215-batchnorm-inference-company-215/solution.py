import numpy as np

def solve(x, mean, var, gamma, beta, eps=1e-5):
    x = np.asarray(x, dtype=float)
    mean = np.asarray(mean, dtype=float)
    var = np.asarray(var, dtype=float)
    gamma = np.asarray(gamma, dtype=float)
    beta = np.asarray(beta, dtype=float)
    return gamma * (x - mean) / np.sqrt(var + eps) + beta
