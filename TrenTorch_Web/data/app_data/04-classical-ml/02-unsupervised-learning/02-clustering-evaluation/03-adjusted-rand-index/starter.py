import numpy as np


def adjusted_rand_index(labels_true: np.ndarray, labels_pred: np.ndarray) -> float:
    """
    Chance-adjusted agreement between two partitions of the same points.
    1.0 for identical partitions, about 0.0 for random ones, and negative
    when worse than chance. Raises ValueError on length mismatch.
    """
    pass
