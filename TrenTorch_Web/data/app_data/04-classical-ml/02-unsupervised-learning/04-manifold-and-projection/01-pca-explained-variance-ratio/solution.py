import numpy as np


def explained_variance_ratio(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if X.ndim != 2 or len(X) < 2:
        raise ValueError("X must be 2-D with at least 2 rows")
    Xc = X - X.mean(axis=0)
    s = np.linalg.svd(Xc, compute_uv=False)
    var = s ** 2
    total = var.sum()
    if total == 0:
        return np.zeros(len(s))
    return var / total
