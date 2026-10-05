import numpy as np

def solve(X):
    X = np.asarray(X, dtype=float)
    lo = X.min(axis=0)
    hi = X.max(axis=0)
    span = hi - lo
    return np.divide(X - lo, span, out=np.zeros_like(X), where=span != 0)
