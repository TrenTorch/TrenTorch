
import numpy as np

from _load import load_solution

pairwise_distances = load_solution("instance-based-probabilistic-knn").pairwise_distances


def region_query(input: np.ndarray, point_idx: int, eps: float) -> np.ndarray:
    distances = pairwise_distances(input, input[point_idx : point_idx + 1])[0]
    return np.where(distances <= eps)[0]


def dbscan_fit(input: np.ndarray, eps: float, min_samples: int) -> np.ndarray:
    n_samples = input.shape[0]
    labels = np.full(n_samples, -1)
    visited = np.zeros(n_samples, dtype=bool)
    cluster_id = 0

    for i in range(n_samples):
        if visited[i]:
            continue
        visited[i] = True

        neighbors = list(region_query(input, i, eps))
        if len(neighbors) < min_samples:
            continue  # stays -1 (noise), may still become a border point later

        labels[i] = cluster_id
        seeds = list(neighbors)
        j = 0
        while j < len(seeds):
            q = seeds[j]
            if not visited[q]:
                visited[q] = True
                q_neighbors = list(region_query(input, q, eps))
                if len(q_neighbors) >= min_samples:
                    seeds.extend(q_neighbors)
            if labels[q] == -1:
                labels[q] = cluster_id
            j += 1

        cluster_id += 1

    return labels
