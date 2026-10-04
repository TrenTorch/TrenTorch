import numpy as np

def solve(f, x, h=1e-05):
    """Implement hessian diagonal according to the contract."""
    x = np.asarray(x, float)
    out = np.zeros_like(x)
    fx = f(x)
    for j in range(len(x)):
        e = np.zeros_like(x)
        e[j] = h
        out[j] = (f(x + e) - 2 * fx + f(x - e)) / (h * h)
    return out
