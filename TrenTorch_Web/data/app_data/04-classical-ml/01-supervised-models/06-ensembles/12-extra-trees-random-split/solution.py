import numpy as np


def _gini(y):
    if len(y) == 0:
        return 0.0
    _, counts = np.unique(y, return_counts=True)
    p = counts / len(y)
    return 1.0 - float(np.sum(p ** 2))


def extra_tree_split(x: np.ndarray, y: np.ndarray, seed: int):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y)
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    lo, hi = float(x.min()), float(x.max())
    if lo == hi:
        return None, 0.0
    rng = np.random.default_rng(seed)
    threshold = rng.uniform(lo, hi)
    left = x <= threshold
    n = len(y)
    nL = int(left.sum())
    nR = n - nL
    if nL == 0 or nR == 0:
        return threshold, 0.0
    gain = _gini(y) - (nL / n) * _gini(y[left]) - (nR / n) * _gini(y[~left])
    return threshold, gain
