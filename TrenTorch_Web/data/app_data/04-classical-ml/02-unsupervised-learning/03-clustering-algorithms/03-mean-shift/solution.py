import numpy as np


def mean_shift(X: np.ndarray, bandwidth: float, max_iter: int = 300, tol: float = 1e-6) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if bandwidth <= 0:
        raise ValueError("bandwidth must be positive")
    modes = X.copy()
    for _ in range(max_iter):
        sq = np.sum((modes[:, None, :] - X[None, :, :]) ** 2, axis=2)
        weights = np.exp(-sq / (2 * bandwidth ** 2))
        new = weights @ X / weights.sum(axis=1, keepdims=True)
        shift = np.max(np.linalg.norm(new - modes, axis=1))
        modes = new
        if shift < tol:
            break
    centers = []
    labels = np.empty(len(X), dtype=int)
    for i, mode in enumerate(modes):
        found = None
        for c, center in enumerate(centers):
            if np.linalg.norm(mode - center) < bandwidth / 2:
                found = c
                break
        if found is None:
            centers.append(mode)
            found = len(centers) - 1
        labels[i] = found
    return labels
