import numpy as np

def solve(f, x, h=1e-5):
    x = np.asarray(x, dtype=float)
    y = np.asarray(f(x), dtype=float).reshape(-1)
    J = np.zeros((len(y), len(x)), dtype=float)
    for j in range(len(x)):
        e = np.zeros_like(x)
        e[j] = h
        J[:, j] = (np.asarray(f(x + e), dtype=float).reshape(-1) - np.asarray(f(x - e), dtype=float).reshape(-1)) / (2 * h)
    return J
