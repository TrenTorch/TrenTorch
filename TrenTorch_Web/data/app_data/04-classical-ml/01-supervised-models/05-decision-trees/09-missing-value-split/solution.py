import numpy as np


def _entropy(labels: np.ndarray) -> float:
    if len(labels) == 0:
        return 0.0
    _, counts = np.unique(labels, return_counts=True)
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())


def fractional_split_gain(x: np.ndarray, y: np.ndarray, threshold: float) -> tuple[float, float]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y)
    if x.ndim != 1 or x.shape != y.shape:
        raise ValueError("x and y must be 1-D with the same length")
    known = ~np.isnan(x)
    n = len(x)
    n_known = int(known.sum())
    if n_known == 0:
        raise ValueError("no observed feature values")
    xk, yk = x[known], y[known]
    left = xk <= threshold
    n_left = int(left.sum())
    weighted = (n_left / n_known) * _entropy(yk[left]) + ((n_known - n_left) / n_known) * _entropy(yk[~left])
    gain = (n_known / n) * (_entropy(yk) - weighted)
    return float(gain), float(n_left / n_known)
