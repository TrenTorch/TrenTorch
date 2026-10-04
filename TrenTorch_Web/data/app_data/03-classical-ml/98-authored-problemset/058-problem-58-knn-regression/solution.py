import numpy as np

def solve(X, y, q, k):
    X = np.asarray(X, dtype=float)
    q = np.asarray(q, dtype=float)
    distances = np.sum((X - q) ** 2, axis=1)
    indices = np.argsort(distances)[:k]
    return float(np.mean(np.asarray(y, dtype=float)[indices]))
