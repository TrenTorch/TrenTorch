import numpy as np


def ecdf(x: np.ndarray) -> tuple:
    values = np.sort(np.asarray(x, dtype=float))
    probabilities = np.arange(1, len(values) + 1) / len(values)
    return values, probabilities


def ecdf_at(x: np.ndarray, points: np.ndarray) -> np.ndarray:
    sorted_x = np.sort(np.asarray(x, dtype=float))
    counts = np.searchsorted(sorted_x, np.asarray(points, dtype=float), side="right")
    return counts / len(sorted_x)


def ks_distance(x: np.ndarray, y: np.ndarray) -> float:
    pooled = np.concatenate([np.asarray(x, dtype=float), np.asarray(y, dtype=float)])
    return float(np.max(np.abs(ecdf_at(x, pooled) - ecdf_at(y, pooled))))
