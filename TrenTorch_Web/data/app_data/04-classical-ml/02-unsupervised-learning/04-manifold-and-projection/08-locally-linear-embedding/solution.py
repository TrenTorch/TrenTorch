import numpy as np


def lle_weights(X: np.ndarray, k: int, reg: float = 1e-3) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if X.ndim != 2:
        raise ValueError("X must be 2-D")
    n = X.shape[0]
    if not 1 <= k < n:
        raise ValueError("k must satisfy 1 <= k < n")
    W = np.zeros((n, n))
    for i in range(n):
        d2 = ((X - X[i]) ** 2).sum(axis=1)
        d2[i] = np.inf
        nbrs = np.argsort(d2, kind="stable")[:k]
        Z = X[nbrs] - X[i]
        G = Z @ Z.T
        trace = np.trace(G)
        eps = reg * trace if trace > 0 else reg
        w = np.linalg.solve(G + eps * np.eye(k), np.ones(k))
        W[i, nbrs] = w / w.sum()
    return W


def lle_embedding(W: np.ndarray, dim: int) -> np.ndarray:
    W = np.asarray(W, dtype=float)
    if W.ndim != 2 or W.shape[0] != W.shape[1]:
        raise ValueError("W must be square")
    n = W.shape[0]
    if not 1 <= dim < n:
        raise ValueError("dim must satisfy 1 <= dim < n")
    I_W = np.eye(n) - W
    M = I_W.T @ I_W
    _, vecs = np.linalg.eigh(M)
    return vecs[:, 1 : dim + 1]
