import numpy as np


def _entropy(labels: np.ndarray) -> float:
    if labels.size == 0:
        return 0.0
    _, counts = np.unique(labels, return_counts=True)
    p = counts / labels.size
    return float(-np.sum(p * np.log2(p)))


def best_threshold(x: np.ndarray, y: np.ndarray) -> tuple:
    distinct = np.unique(x)
    if distinct.size < 2:
        return None, 0.0
    parent = _entropy(y)
    best_t, best_gain = None, -1.0
    for t in (distinct[:-1] + distinct[1:]) / 2.0:
        left, right = y[x <= t], y[x > t]
        gain = parent - (left.size * _entropy(left) + right.size * _entropy(right)) / y.size
        if gain > best_gain + 1e-12:
            best_t, best_gain = float(t), float(gain)
    return best_t, best_gain
