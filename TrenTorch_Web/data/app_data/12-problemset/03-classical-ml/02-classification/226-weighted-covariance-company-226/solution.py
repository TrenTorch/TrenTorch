import numpy as np

def solve(X, w):
    X = np.asarray(X, dtype=float)
    w = np.asarray(w, dtype=float)
    p = w / w.sum()
    mu = (p[:, None] * X).sum(axis=0)
    Z = X - mu
    return (Z * p[:, None]).T @ Z
