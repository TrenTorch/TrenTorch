import numpy as np


def classical_mds(D: np.ndarray, k: int) -> np.ndarray:
    D = np.asarray(D, dtype=float)
    if D.ndim != 2 or D.shape[0] != D.shape[1]:
        raise ValueError("D must be square")
    if not np.allclose(D, D.T) or not np.allclose(np.diag(D), 0.0):
        raise ValueError("D must be symmetric with a zero diagonal")
    n = len(D)
    if not 1 <= k <= n:
        raise ValueError("k must satisfy 1 <= k <= number of points")
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D ** 2) @ J
    vals, vecs = np.linalg.eigh(B)
    order = np.argsort(vals)[::-1][:k]
    vals = np.clip(vals[order], 0.0, None)
    return vecs[:, order] * np.sqrt(vals)
