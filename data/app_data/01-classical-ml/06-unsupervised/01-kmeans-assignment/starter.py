import numpy as np


def kmeans_assign(input: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    """
    input:     shape (n_samples, n_features)
    centroids: shape (k, n_features)

    Returns:
        shape (n_samples,): the index of the nearest centroid for every
        sample.
    """
    # TODO: Reuse 01-knn's pairwise_distances between centroids and
    # input, then argmin over the centroid axis for each sample.
    pass
