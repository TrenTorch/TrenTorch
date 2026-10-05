import numpy as np


def percentiles(a: np.ndarray, qs) -> np.ndarray:
    return np.percentile(a, qs)


def iqr(a: np.ndarray) -> float:
    q1, q3 = np.percentile(a, [25, 75])
    return float(q3 - q1)


def zscores(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    std = a.std()
    if std == 0:
        return np.zeros_like(a)
    return (a - a.mean()) / std


def pearson(x: np.ndarray, y: np.ndarray) -> float:
    xc = np.asarray(x, dtype=float) - np.mean(x)
    yc = np.asarray(y, dtype=float) - np.mean(y)
    return float((xc * yc).sum() / np.sqrt((xc**2).sum() * (yc**2).sum()))


def covariance_matrix(x: np.ndarray) -> np.ndarray:
    xc = np.asarray(x, dtype=float) - np.mean(x, axis=0)
    return xc.T @ xc / (len(xc) - 1)
