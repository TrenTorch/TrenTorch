import numpy as np


def davies_bouldin_index(X: np.ndarray, labels: np.ndarray) -> float:
    """
    Mean over clusters of the worst (S_i + S_j) / d(c_i, c_j) ratio.
    Lower is better. Raises ValueError when there are fewer than two clusters.
    """
    pass
