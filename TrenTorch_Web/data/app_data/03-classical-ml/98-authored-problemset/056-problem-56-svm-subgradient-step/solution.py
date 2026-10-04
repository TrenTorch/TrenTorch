import numpy as np

def solve(X, y, w, lr, reg):
    """Implement svm subgradient step according to the contract."""
    X, y, w = (np.asarray(X, float), np.asarray(y, float), np.asarray(w, float).copy())
    margins = y * (X @ w)
    mask = margins < 1
    w -= lr * (w - reg * np.sum(X[mask] * y[mask, None], axis=0))
    return w
