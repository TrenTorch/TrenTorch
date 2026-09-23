import numpy as np


def kmeans_update_centroids(
    input: np.ndarray, assignments: np.ndarray, centroids: np.ndarray
) -> np.ndarray:
    n_clusters = centroids.shape[0]
    new_centroids = centroids.copy()
    for cluster in range(n_clusters):
        members = input[assignments == cluster]
        if members.shape[0] > 0:
            new_centroids[cluster] = members.mean(axis=0)
    return new_centroids
