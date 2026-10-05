import numpy as np


def isomap(X: np.ndarray, n_neighbors: int, n_components: int) -> np.ndarray:
    """
    Isomap embedding of shape (n, n_components). Uses a symmetric k-nearest
    neighbor graph, Floyd-Warshall geodesics, then classical MDS. Raises
    ValueError for out-of-range arguments or a disconnected graph.
    """
    pass
