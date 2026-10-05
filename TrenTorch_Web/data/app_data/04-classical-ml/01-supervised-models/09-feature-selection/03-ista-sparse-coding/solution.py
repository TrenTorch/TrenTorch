import numpy as np


def soft_threshold(z: np.ndarray, t: float) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    return np.sign(z) * np.maximum(np.abs(z) - t, 0.0)


def sparse_code(D: np.ndarray, y: np.ndarray, lam: float = 0.1, iters: int = 100) -> np.ndarray:
    D = np.asarray(D, dtype=float)
    y = np.asarray(y, dtype=float)
    if D.ndim != 2 or y.ndim != 1 or len(y) != D.shape[0]:
        raise ValueError("D must be 2-D and y must have one entry per row of D")
    if lam < 0 or iters < 0:
        raise ValueError("lam and iters must be nonnegative")
    L = np.linalg.norm(D, 2) ** 2
    step = 1.0 / L if L > 0 else 1.0
    x = np.zeros(D.shape[1])
    for _ in range(iters):
        g = D.T @ (D @ x - y)
        x = soft_threshold(x - step * g, step * lam)
    return x
