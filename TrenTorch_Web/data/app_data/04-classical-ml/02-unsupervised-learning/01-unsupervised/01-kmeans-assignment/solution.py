
import numpy as np

from _load import load_solution

pairwise_distances = load_solution("instance-based-probabilistic-knn").pairwise_distances


def kmeans_assign(input: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    distances = pairwise_distances(centroids, input)
    return np.argmin(distances, axis=1)
