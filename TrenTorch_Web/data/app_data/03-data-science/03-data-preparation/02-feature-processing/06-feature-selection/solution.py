import numpy as np


def _standardize(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    std = a.std(axis=0)
    safe = np.where(std == 0.0, 1.0, std)
    return (a - a.mean(axis=0)) / safe


def variance_threshold(x: np.ndarray, threshold: float = 0.0) -> np.ndarray:
    return np.asarray(x, dtype=float).var(axis=0) > threshold


def drop_correlated(x: np.ndarray, threshold: float) -> list:
    z = _standardize(x)
    n = z.shape[0]
    kept = []
    for j in range(z.shape[1]):
        correlations = [abs(float(z[:, j] @ z[:, i]) / n) for i in kept]
        if all(c <= threshold for c in correlations):
            kept.append(j)
    return kept


def select_k_best(x: np.ndarray, y: np.ndarray, k: int) -> np.ndarray:
    zx = _standardize(x)
    zy = _standardize(np.asarray(y, dtype=float).reshape(-1, 1))[:, 0]
    scores = np.abs(zx.T @ zy) / len(zy)
    order = np.argsort(-scores, kind="stable")
    return order[:k]
