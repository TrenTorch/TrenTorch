import numpy as np


def affinity_propagation(X: np.ndarray, preference=None, damping: float = 0.5, max_iter: int = 200) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if not 0.5 <= damping < 1:
        raise ValueError("damping must be in [0.5, 1)")
    n = len(X)
    if n == 1:
        return np.zeros(1, dtype=int)
    S = -np.sum((X[:, None, :] - X[None, :, :]) ** 2, axis=2)
    off = S[~np.eye(n, dtype=bool)]
    p = np.median(off) if preference is None else preference
    np.fill_diagonal(S, p)

    R = np.zeros((n, n))
    A = np.zeros((n, n))
    rows = np.arange(n)
    for _ in range(max_iter):
        AS = A + S
        idx = np.argmax(AS, axis=1)
        first = AS[rows, idx].copy()
        AS[rows, idx] = -np.inf
        second = AS.max(axis=1)
        maxes = np.repeat(first[:, None], n, axis=1)
        maxes[rows, idx] = second
        R = damping * R + (1 - damping) * (S - maxes)

        Rp = np.maximum(R, 0)
        np.fill_diagonal(Rp, np.diag(R))
        colsum = Rp.sum(axis=0)
        A_new = np.minimum(colsum[None, :] - Rp, 0)
        np.fill_diagonal(A_new, colsum - np.diag(Rp))
        A = damping * A + (1 - damping) * A_new

    scores = np.diag(A + R)
    exemplars = np.flatnonzero(scores > 0)
    if len(exemplars) == 0:
        exemplars = np.array([int(np.argmax(scores))])
    labels = np.argmax(S[:, exemplars], axis=1)
    for j, e in enumerate(exemplars):
        labels[e] = j
    return labels
