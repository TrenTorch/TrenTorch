import numpy as np

def solve(x):
    """Implement min-max scaling according to the contract."""
    X = np.asarray(x, float)
    lo, hi = (X.min(0), X.max(0))
    span = hi - lo
    return np.divide(X - lo, span, out=np.zeros_like(X), where=span != 0)
