import numpy as np


def davies_bouldin_index(X: np.ndarray, labels: np.ndarray) -> float:
    X = np.asarray(X, dtype=float)
    labels = np.asarray(labels)
    clusters = np.unique(labels)
    if len(clusters) < 2:
        raise ValueError("Davies-Bouldin needs at least two clusters")
    centroids = np.array([X[labels == c].mean(axis=0) for c in clusters])
    scatter = np.array(
        [np.mean(np.linalg.norm(X[labels == c] - centroids[i], axis=1)) for i, c in enumerate(clusters)]
    )
    separation = np.linalg.norm(centroids[:, None, :] - centroids[None, :, :], axis=2)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = (scatter[:, None] + scatter[None, :]) / separation
    np.fill_diagonal(ratio, -np.inf)
    return float(np.mean(np.max(ratio, axis=1)))
