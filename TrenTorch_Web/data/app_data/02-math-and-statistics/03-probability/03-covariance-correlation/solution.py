import numpy as np


def covariance(x: np.ndarray, y: np.ndarray, ddof: int = 0) -> float:
    n = len(x)
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    return float(np.sum((x - mean_x) * (y - mean_y)) / (n - ddof))


def correlation(x: np.ndarray, y: np.ndarray) -> float:
    return float(covariance(x, y) / (np.std(x) * np.std(y)))
