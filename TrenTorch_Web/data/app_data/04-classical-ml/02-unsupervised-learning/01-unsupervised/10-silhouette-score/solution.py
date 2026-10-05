import numpy as np


def silhouette_score(X: np.ndarray, labels: np.ndarray) -> float:
    X = np.asarray(X, dtype=float)
    labels = np.asarray(labels)
    clusters = np.unique(labels)
    if clusters.size < 2:
        return 0.0
    distances = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
    scores = np.zeros(len(X))
    for i in range(len(X)):
        same = labels == labels[i]
        if same.sum() == 1:
            continue
        a = distances[i, same].sum() / (same.sum() - 1)
        b = min(distances[i, labels == c].mean() for c in clusters if c != labels[i])
        denominator = max(a, b)
        scores[i] = 0.0 if denominator == 0 else (b - a) / denominator
    return float(scores.mean())
