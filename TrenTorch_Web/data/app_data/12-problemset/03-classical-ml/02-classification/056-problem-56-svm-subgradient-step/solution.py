import numpy as np

def solve(X, y, w, lr, reg):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    w = np.asarray(w, dtype=float).copy()
    margins = y * (X @ w)
    active = margins < 1
    gradient = w - reg * np.sum(X[active] * y[active, None], axis=0)
    return w - lr * gradient
