import numpy as np


def isomap(X: np.ndarray, n_neighbors: int, n_components: int) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    n = len(X)
    if not 1 <= n_neighbors < n:
        raise ValueError("n_neighbors must satisfy 1 <= n_neighbors < number of rows")
    if not 1 <= n_components <= n:
        raise ValueError("n_components must satisfy 1 <= n_components <= number of rows")

    E = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
    G = np.full((n, n), np.inf)
    nearest = np.argsort(E, axis=1)[:, 1:n_neighbors + 1]
    for i in range(n):
        G[i, nearest[i]] = E[i, nearest[i]]
    G = np.minimum(G, G.T)
    np.fill_diagonal(G, 0.0)

    for k in range(n):
        G = np.minimum(G, G[:, [k]] + G[[k], :])
    if not np.all(np.isfinite(G)):
        raise ValueError("neighbor graph is disconnected")

    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (G ** 2) @ J
    vals, vecs = np.linalg.eigh(B)
    order = np.argsort(vals)[::-1][:n_components]
    vals = np.clip(vals[order], 0.0, None)
    return vecs[:, order] * np.sqrt(vals)
