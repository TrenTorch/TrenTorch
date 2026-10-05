import numpy as np


def k_medoids(X: np.ndarray, k: int, max_iter: int = 100, seed: int = 0):
    X = np.asarray(X, dtype=float)
    n = len(X)
    if not 1 <= k <= n:
        raise ValueError("k must satisfy 1 <= k <= number of samples")
    D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
    rng = np.random.default_rng(seed)
    medoids = rng.choice(n, size=k, replace=False)
    for _ in range(max_iter):
        labels = np.argmin(D[:, medoids], axis=1)
        new = medoids.copy()
        for c in range(k):
            members = np.flatnonzero(labels == c)
            if len(members) == 0:
                continue
            costs = D[np.ix_(members, members)].sum(axis=1)
            new[c] = members[np.argmin(costs)]
        if np.array_equal(new, medoids):
            break
        medoids = new
    labels = np.argmin(D[:, medoids], axis=1)
    return labels, medoids
