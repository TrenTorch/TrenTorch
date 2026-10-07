import numpy as np

def solve(f, x, analytic, h=1e-5):
    x = np.asarray(x, dtype=float)
    analytic = np.asarray(analytic, dtype=float)
    xp = x.copy()
    xm = x.copy()
    xp[0] += h
    xm[0] -= h
    numeric = (f(xp) - f(xm)) / (2 * h)
    return float(numeric), float(analytic[0]), float(abs(numeric - analytic[0]))
