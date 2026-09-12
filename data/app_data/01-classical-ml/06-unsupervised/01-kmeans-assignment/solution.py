import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

pairwise_distances = load_solution(
    "01-classical-ml/05-instance-based-probabilistic/01-knn"
).pairwise_distances


def kmeans_assign(input: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    distances = pairwise_distances(centroids, input)
    return np.argmin(distances, axis=1)
