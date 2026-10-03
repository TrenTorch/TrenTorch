import numpy as np


def omp(D: np.ndarray, y: np.ndarray, k: int) -> np.ndarray:
    D = np.asarray(D, dtype=float)
    y = np.asarray(y, dtype=float)
    if D.ndim != 2 or y.ndim != 1 or len(y) != D.shape[0]:
        raise ValueError("D must be 2-D and y must have one entry per row of D")
    n, d = D.shape
    if k < 0 or k > d:
        raise ValueError("k must be between 0 and the number of columns")
    x = np.zeros(d)
    support = []
    residual = y.copy()
    coef = np.zeros(0)
    for _ in range(k):
        corr = np.abs(D.T @ residual)
        corr[support] = -np.inf
        support.append(int(np.argmax(corr)))
        coef, *_ = np.linalg.lstsq(D[:, support], y, rcond=None)
        residual = y - D[:, support] @ coef
    if support:
        x[support] = coef
    return x
