import numpy as np


def zca_whiten(X: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if len(X) < 2:
        raise ValueError("X must have at least 2 rows")
    if eps < 0:
        raise ValueError("eps must be nonnegative")
    Xc = X - X.mean(axis=0)
    C = Xc.T @ Xc / (len(X) - 1)
    vals, vecs = np.linalg.eigh(C)
    W = (vecs * (1.0 / np.sqrt(vals + eps))) @ vecs.T
    return Xc @ W
