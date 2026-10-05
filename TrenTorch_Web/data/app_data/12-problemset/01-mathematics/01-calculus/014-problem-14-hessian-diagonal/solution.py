import numpy as np

def solve(f, x, h=1e-5):
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    fx = f(x)
    for j in range(len(x)):
        e = np.zeros_like(x)
        e[j] = h
        out[j] = (f(x + e) - 2 * fx + f(x - e)) / (h * h)
    return out
