import numpy as np


def calinski_harabasz_index(X: np.ndarray, labels: np.ndarray) -> float:
    """
    (B / (k - 1)) / (W / (n - k)): between-cluster over within-cluster
    dispersion. Raises ValueError unless 2 <= k < n. Returns inf when W is 0.
    """
    pass
