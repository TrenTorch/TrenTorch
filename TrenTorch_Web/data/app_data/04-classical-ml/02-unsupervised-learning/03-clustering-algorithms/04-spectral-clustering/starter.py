import numpy as np


def spectral_clustering(W: np.ndarray, k: int) -> np.ndarray:
    """
    Cluster the nodes of a weighted undirected graph given by affinity
    matrix W. Uses the k smallest eigenvectors of the normalized Laplacian,
    row-normalized, then deterministic farthest-first k-means.
    Raises ValueError when W is not square and symmetric, or k is out of range.
    """
    pass
