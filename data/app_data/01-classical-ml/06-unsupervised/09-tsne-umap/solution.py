import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

pairwise_distances = load_solution(
    "01-classical-ml/05-instance-based-probabilistic/01-knn"
).pairwise_distances


def gaussian_affinities(input: np.ndarray, sigma: float) -> np.ndarray:
    distances = pairwise_distances(input, input)

    unnormalized = np.exp(-(distances**2) / (2 * sigma**2))
    np.fill_diagonal(unnormalized, 0.0)

    row_sums = unnormalized.sum(axis=1, keepdims=True)
    return unnormalized / row_sums
