import numpy as np


def region_query(input: np.ndarray, point_idx: int, eps: float) -> np.ndarray:
    """
    Returns:
        the indices of every row of input within eps (inclusive) of
        input[point_idx], including point_idx itself.
    """
    # TODO: Reuse 01-knn's pairwise_distances between input and the
    # single point input[point_idx], then np.where the distances <= eps.
    pass


def dbscan_fit(input: np.ndarray, eps: float, min_samples: int) -> np.ndarray:
    """
    Returns:
        shape (n_samples,): a cluster id (0, 1, 2, ...) per sample, or
        -1 for noise (a point that never joins any cluster).
    """
    # TODO: Standard DBSCAN. labels start at -1 (noise) for everyone,
    # visited starts all False, cluster_id starts at 0. For each
    # unvisited point i: mark visited, region_query it. Fewer than
    # min_samples neighbors -> leave it noise for now, continue to the
    # next point. Otherwise it's a core point: start a new cluster,
    # then grow it breadth-first through its neighbors' neighbors
    # (only expanding through points that ALSO have >= min_samples
    # neighbors -- other points still join the cluster as border
    # points, but don't expand it further), labeling every point
    # reached along the way with this cluster_id. Increment cluster_id
    # once the cluster is fully grown.
    pass
