import numpy as np

def solve(X, i, eps):
    """Implement dbscan region query according to the contract."""
    X = np.asarray(X, float)
    d = np.sum((X - X[i]) ** 2, axis=1)
    return np.where(d <= eps ** 2)[0]
