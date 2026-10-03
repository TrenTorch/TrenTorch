import numpy as np


def propagate(W: np.ndarray, Y0: np.ndarray, alpha: float, iters: int) -> np.ndarray:
    W = np.asarray(W, dtype=float)
    Y = np.asarray(Y0, dtype=float)
    if W.ndim != 2 or W.shape[0] != W.shape[1]:
        raise ValueError("W must be square")
    if not np.allclose(W, W.T):
        raise ValueError("W must be symmetric")
    if np.any(W < 0):
        raise ValueError("W must be nonnegative")
    if Y.ndim != 2 or Y.shape[0] != W.shape[0]:
        raise ValueError("Y0 must have one row per node")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must lie in (0, 1)")
    if iters < 0:
        raise ValueError("iters must be nonnegative")
    degree = W.sum(axis=1)
    if np.any(degree <= 0):
        raise ValueError("every node needs positive degree")
    d_inv_sqrt = 1.0 / np.sqrt(degree)
    S = d_inv_sqrt[:, None] * W * d_inv_sqrt[None, :]
    F = Y.copy()
    for _ in range(iters):
        F = alpha * (S @ F) + (1.0 - alpha) * Y
    return F
