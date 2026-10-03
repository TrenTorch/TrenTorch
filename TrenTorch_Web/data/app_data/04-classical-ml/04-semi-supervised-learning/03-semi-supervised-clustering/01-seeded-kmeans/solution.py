import numpy as np


def seeded_kmeans(X: np.ndarray, seeds: np.ndarray, k: int, iters: int = 100):
    X = np.asarray(X, dtype=float)
    seeds = np.asarray(seeds, dtype=int)
    if X.ndim != 2 or seeds.shape != (X.shape[0],):
        raise ValueError("X must be (N, d) and seeds must be (N,)")
    if k < 1 or iters < 1:
        raise ValueError("k and iters must be at least 1")
    if np.any((seeds < -1) | (seeds >= k)):
        raise ValueError("seed labels must be -1 or in 0..k-1")
    seeded = seeds >= 0
    centroids = np.zeros((k, X.shape[1]))
    for c in range(k):
        members = seeds == c
        if not members.any():
            raise ValueError(f"class {c} has no seed")
        centroids[c] = X[members].mean(axis=0)
    labels = seeds.copy()
    for _ in range(iters):
        dist = ((X[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
        new_labels = dist.argmin(axis=1)
        new_labels[seeded] = seeds[seeded]
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
        for c in range(k):
            centroids[c] = X[labels == c].mean(axis=0)
    return labels, centroids
