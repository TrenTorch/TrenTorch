import numpy as np


def kmeans_update_centroids(
    input: np.ndarray, assignments: np.ndarray, centroids: np.ndarray
) -> np.ndarray:
    """
    input:       shape (n_samples, n_features)
    assignments: shape (n_samples,), from 01-kmeans-assignment's kmeans_assign
    centroids:   shape (k, n_features), the CURRENT centroids

    Returns:
        shape (k, n_features): each centroid moved to the mean of the
        points currently assigned to it. A cluster with zero points
        assigned keeps its OLD centroid unchanged, an empty mean is
        undefined.
    """
    # TODO: For each cluster index, average the input rows whose
    # assignment equals that index. If no rows are assigned to a
    # cluster, leave that cluster's centroid as it was.
    pass
