import numpy as np


def truncated_svd(X: np.ndarray, k: int):
    X = np.asarray(X, dtype=float)
    if not 1 <= k <= min(X.shape):
        raise ValueError("k must satisfy 1 <= k <= min(n, d)")
    U, s, Vt = np.linalg.svd(X, full_matrices=False)
    return U[:, :k], s[:k], Vt[:k]
