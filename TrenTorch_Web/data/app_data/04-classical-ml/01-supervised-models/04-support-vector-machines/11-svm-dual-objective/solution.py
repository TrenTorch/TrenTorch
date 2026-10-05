import numpy as np


def dual_objective(alpha: np.ndarray, y: np.ndarray, K: np.ndarray) -> float:
    alpha = np.asarray(alpha, dtype=float)
    y = np.asarray(y, dtype=float)
    K = np.asarray(K, dtype=float)
    n = len(alpha)
    if y.shape != (n,) or K.shape != (n, n):
        raise ValueError("alpha and y must have length n and K must be n by n")
    ay = alpha * y
    return float(alpha.sum() - 0.5 * ay @ K @ ay)


def is_dual_feasible(alpha: np.ndarray, y: np.ndarray, C: float, tol: float = 1e-9) -> bool:
    alpha = np.asarray(alpha, dtype=float)
    y = np.asarray(y, dtype=float)
    if C < 0:
        raise ValueError("C must be nonnegative")
    if alpha.shape != y.shape:
        raise ValueError("alpha and y must have the same shape")
    in_box = np.all(alpha >= -tol) and np.all(alpha <= C + tol)
    balanced = abs(alpha @ y) <= tol
    return bool(in_box and balanced)
