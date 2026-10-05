import numpy as np


def calinski_harabasz_index(X: np.ndarray, labels: np.ndarray) -> float:
    X = np.asarray(X, dtype=float)
    labels = np.asarray(labels)
    n = len(X)
    clusters = np.unique(labels)
    k = len(clusters)
    if k < 2 or k >= n:
        raise ValueError("Calinski-Harabasz needs 2 <= clusters < samples")
    overall = X.mean(axis=0)
    between = 0.0
    within = 0.0
    for c in clusters:
        members = X[labels == c]
        centroid = members.mean(axis=0)
        between += len(members) * np.sum((centroid - overall) ** 2)
        within += np.sum((members - centroid) ** 2)
    if within == 0:
        return float("inf")
    return float((between / (k - 1)) / (within / (n - k)))
