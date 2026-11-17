import numpy as np

def solve(X, y, w, b, lam):
    residual = np.asarray(X, dtype=float) @ np.asarray(w, dtype=float) + b - np.asarray(y, dtype=float)
    return float(np.mean(residual ** 2) + lam * np.sum(np.asarray(w, dtype=float) ** 2))
