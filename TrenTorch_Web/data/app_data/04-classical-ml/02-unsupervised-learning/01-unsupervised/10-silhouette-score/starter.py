import numpy as np


def silhouette_score(X: np.ndarray, labels: np.ndarray) -> float:
    """
    X: (n_samples, n_features) points.
    labels: (n_samples,) cluster ids.

    Returns:
        mean silhouette coefficient (Euclidean), 0.0 if fewer than 2 clusters.
    """
    # TODO: Compute a(i), b(i) and s(i) for every point, then average.
    pass
