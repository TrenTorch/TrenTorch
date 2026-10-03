import numpy as np


def spectral_clustering(W: np.ndarray, k: int) -> np.ndarray:
    W = np.asarray(W, dtype=float)
    if W.ndim != 2 or W.shape[0] != W.shape[1]:
        raise ValueError("W must be square")
    if not np.allclose(W, W.T):
        raise ValueError("W must be symmetric")
    n = len(W)
    if not 1 <= k <= n:
        raise ValueError("k must satisfy 1 <= k <= number of nodes")
    degree = W.sum(axis=1)
    inv_sqrt = np.where(degree > 0, 1.0 / np.sqrt(np.where(degree > 0, degree, 1.0)), 0.0)
    L = np.eye(n) - inv_sqrt[:, None] * W * inv_sqrt[None, :]
    _, vectors = np.linalg.eigh(L)
    U = vectors[:, :k]
    norms = np.linalg.norm(U, axis=1, keepdims=True)
    U = np.where(norms > 0, U / np.where(norms > 0, norms, 1.0), 0.0)

    chosen = [0]
    while len(chosen) < k:
        dist = np.min(np.linalg.norm(U[:, None, :] - U[chosen][None, :, :], axis=2), axis=1)
        chosen.append(int(np.argmax(dist)))
    centers = U[chosen].copy()

    labels = np.full(n, -1)
    for _ in range(100):
        new_labels = np.argmin(np.linalg.norm(U[:, None, :] - centers[None, :, :], axis=2), axis=1)
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
        for c in range(k):
            members = U[labels == c]
            if len(members):
                centers[c] = members.mean(axis=0)
    return labels
