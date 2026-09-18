import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

pairwise_distances = load_solution(
    "01-classical-ml/05-instance-based-probabilistic/01-knn"
).pairwise_distances


def cluster_distance(points_a: np.ndarray, points_b: np.ndarray, linkage: str) -> float:
    distances = pairwise_distances(points_a, points_b)
    if linkage == "single":
        return float(distances.min())
    elif linkage == "complete":
        return float(distances.max())
    elif linkage == "average":
        return float(distances.mean())
    raise ValueError(f"Unknown linkage: {linkage!r}")


def agglomerative_fit(input: np.ndarray, n_clusters: int, linkage: str = "single") -> np.ndarray:
    n_samples = input.shape[0]
    clusters = [[i] for i in range(n_samples)]

    while len(clusters) > n_clusters:
        best_distance = np.inf
        best_pair = (0, 1)
        for a in range(len(clusters)):
            for b in range(a + 1, len(clusters)):
                distance = cluster_distance(input[clusters[a]], input[clusters[b]], linkage)
                if distance < best_distance:
                    best_distance = distance
                    best_pair = (a, b)

        a, b = best_pair
        clusters[a] = clusters[a] + clusters[b]
        del clusters[b]

    labels = np.empty(n_samples, dtype=int)
    for cluster_id, members in enumerate(clusters):
        for member in members:
            labels[member] = cluster_id
    return labels
