import numpy as np

def solve(X, y, w, b, lam):
    """Implement ridge objective according to the contract."""
    r = np.asarray(X) @ np.asarray(w) + b - np.asarray(y)
    return float(np.mean(r * r) + lam * np.sum(np.asarray(w) ** 2))
