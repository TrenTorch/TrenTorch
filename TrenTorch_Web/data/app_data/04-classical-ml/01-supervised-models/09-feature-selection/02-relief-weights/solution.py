import numpy as np


def relief_weights(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    if X.ndim != 2 or X.shape[0] < 2 or len(y) != X.shape[0]:
        raise ValueError("X must be 2-D with at least two rows, and y must have one label per row")
    n, d = X.shape
    spread = X.max(axis=0) - X.min(axis=0)
    scale = np.where(spread > 0, spread, 1.0)
    w = np.zeros(d)
    for i in range(n):
        dist = np.sqrt(((X - X[i]) ** 2).sum(axis=1))
        dist[i] = np.inf
        same = np.where(y == y[i])[0]
        same = same[same != i]
        other = np.where(y != y[i])[0]
        if len(same) == 0 or len(other) == 0:
            continue
        hit = same[np.argmin(dist[same])]
        miss = other[np.argmin(dist[other])]
        w += (np.abs(X[i] - X[miss]) - np.abs(X[i] - X[hit])) / scale
    return w / n
