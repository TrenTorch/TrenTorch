import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

pairwise_distances = load_solution(
    "04-classical-ml/01-supervised-models/07-instance-based-probabilistic/01-knn"
).pairwise_distances


def kmeans_assign(input: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    distances = pairwise_distances(centroids, input)
    return np.argmin(distances, axis=1)
