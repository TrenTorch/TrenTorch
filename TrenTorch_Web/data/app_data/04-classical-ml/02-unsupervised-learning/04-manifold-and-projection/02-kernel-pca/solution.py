import numpy as np


def kernel_pca(X: np.ndarray, n_components: int, gamma=None) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    n = len(X)
    if not 1 <= n_components <= n:
        raise ValueError("n_components must satisfy 1 <= n_components <= number of rows")
    if gamma is not None and gamma <= 0:
        raise ValueError("gamma must be positive")
    if gamma is None:
        K = X @ X.T
    else:
        sq = np.sum((X[:, None, :] - X[None, :, :]) ** 2, axis=2)
        K = np.exp(-gamma * sq)
    one = np.full((n, n), 1.0 / n)
    Kc = K - one @ K - K @ one + one @ K @ one
    vals, vecs = np.linalg.eigh(Kc)
    order = np.argsort(vals)[::-1][:n_components]
    vals = np.clip(vals[order], 0.0, None)
    return vecs[:, order] * np.sqrt(vals)
