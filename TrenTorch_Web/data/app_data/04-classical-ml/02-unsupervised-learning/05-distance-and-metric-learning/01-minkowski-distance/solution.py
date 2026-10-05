import numpy as np


def minkowski(x: np.ndarray, y: np.ndarray, p: float) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or x.shape != y.shape:
        raise ValueError("x and y must be 1-D with the same length")
    if p < 1:
        raise ValueError("p must be at least 1")
    diff = np.abs(x - y)
    if np.isinf(p):
        return float(diff.max(initial=0.0))
    return float(np.sum(diff ** p) ** (1.0 / p))
