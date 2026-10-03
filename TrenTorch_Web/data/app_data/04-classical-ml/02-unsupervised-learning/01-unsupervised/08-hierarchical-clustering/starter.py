import numpy as np


def cluster_distance(points_a: np.ndarray, points_b: np.ndarray, linkage: str) -> float:
    """
    points_a, points_b: two groups of rows (two clusters' worth of points).
    linkage: 'single' (closest pair), 'complete' (farthest pair), or
    'average' (mean of every pair) between the two groups.
    """
    # TODO: Reuse 01-knn's pairwise_distances between points_a and
    # points_b, then min/max/mean the whole matrix depending on linkage.
    # Raise ValueError for anything else.
    pass


def agglomerative_fit(input: np.ndarray, n_clusters: int, linkage: str = "single") -> np.ndarray:
    """
    Returns:
        shape (n_samples,): a cluster id (0..n_clusters-1) per sample.
    """
    # TODO: Start with every sample as its own singleton cluster.
    # Repeat until only n_clusters clusters remain: find the pair of
    # clusters with the smallest cluster_distance(), merge them into
    # one (concatenate their member indices), remove the old pair.
    # Finally assign each sample the id of whichever final cluster it
    # ended up in.
    pass
