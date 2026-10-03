import numpy as np


def fuzzy_c_means(X: np.ndarray, c: int, m: float = 2.0, max_iter: int = 100, tol: float = 1e-5):
    X = np.asarray(X, dtype=float)
    if m <= 1:
        raise ValueError("m must be greater than 1")
    n = len(X)
    if not 1 <= c <= n:
        raise ValueError("c must satisfy 1 <= c <= number of rows")

    chosen = [0]
    while len(chosen) < c:
        dist = np.min(np.linalg.norm(X[:, None, :] - X[chosen][None, :, :], axis=2), axis=1)
        chosen.append(int(np.argmax(dist)))
    centers = X[chosen].copy()

    U = None
    for _ in range(max_iter):
        D = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2)
        new_U = np.zeros((n, c))
        zero = D == 0
        exact = zero.any(axis=1)
        new_U[exact] = zero[exact] / zero[exact].sum(axis=1, keepdims=True)
        safe = ~exact
        Ds = np.where(zero, 1.0, D)[safe]
        ratio = (Ds[:, :, None] / Ds[:, None, :]) ** (2.0 / (m - 1))
        new_U[safe] = 1.0 / ratio.sum(axis=2)

        if U is not None and np.max(np.abs(new_U - U)) < tol:
            U = new_U
            break
        U = new_U
        W = U ** m
        centers = (W.T @ X) / W.sum(axis=0)[:, None]
    return centers, U
