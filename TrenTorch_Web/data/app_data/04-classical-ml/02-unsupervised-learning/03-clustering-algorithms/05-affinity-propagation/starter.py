import numpy as np


def affinity_propagation(X: np.ndarray, preference=None, damping: float = 0.5, max_iter: int = 200) -> np.ndarray:
    """
    Cluster rows of X with affinity propagation on negative squared Euclidean
    similarities. Returns integer labels 0..m-1 where m is the number of
    exemplars. Raises ValueError when damping is outside [0.5, 1).
    """
    pass
