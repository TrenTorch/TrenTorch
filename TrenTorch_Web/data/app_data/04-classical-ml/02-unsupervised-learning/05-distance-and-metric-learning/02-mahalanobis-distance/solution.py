import numpy as np


def mahalanobis(x: np.ndarray, y: np.ndarray, cov: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    cov = np.asarray(cov, dtype=float)
    d = x.shape[0] if x.ndim == 1 else -1
    if x.ndim != 1 or x.shape != y.shape or cov.shape != (d, d):
        raise ValueError("x and y must have length d and cov must be d by d")
    if not np.allclose(cov, cov.T):
        raise ValueError("cov must be symmetric")
    try:
        L = np.linalg.cholesky(cov)
    except np.linalg.LinAlgError as err:
        raise ValueError("cov must be positive definite") from err
    z = np.linalg.solve(L, x - y)
    return float(np.sqrt(z @ z))
