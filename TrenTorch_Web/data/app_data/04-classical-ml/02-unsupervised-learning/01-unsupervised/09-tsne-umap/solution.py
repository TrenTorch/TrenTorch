
import numpy as np

from _load import load_solution

pairwise_distances = load_solution("instance-based-probabilistic-knn").pairwise_distances


def gaussian_affinities(input: np.ndarray, sigma: float) -> np.ndarray:
    distances = pairwise_distances(input, input)

    unnormalized = np.exp(-(distances**2) / (2 * sigma**2))
    np.fill_diagonal(unnormalized, 0.0)

    row_sums = unnormalized.sum(axis=1, keepdims=True)
    return unnormalized / row_sums
