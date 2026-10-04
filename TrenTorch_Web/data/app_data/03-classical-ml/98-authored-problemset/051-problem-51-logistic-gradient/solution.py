import numpy as np

def solve(X, y, w):
    """Implement logistic gradient according to the contract."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    p = 1 / (1 + np.exp(-X @ w))
    r = p - y
    return (X.T @ r / len(y), float(r.mean()))
