import numpy as np


def _gini(labels: np.ndarray) -> float:
    if len(labels) == 0:
        return 0.0
    _, counts = np.unique(labels, return_counts=True)
    p = counts / counts.sum()
    return float(1.0 - (p ** 2).sum())


def oblique_split_gain(X: np.ndarray, y: np.ndarray, w: np.ndarray, b: float) -> float:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    w = np.asarray(w, dtype=float)
    if X.ndim != 2 or w.shape != (X.shape[1],) or y.shape != (X.shape[0],):
        raise ValueError("X is (n, d), w is (d,), and y is (n,)")
    if not np.any(w):
        raise ValueError("w must be nonzero")
    n = len(y)
    left = X @ w + b <= 0
    gain = _gini(y) - (left.sum() / n) * _gini(y[left]) - ((~left).sum() / n) * _gini(y[~left])
    return float(gain)
