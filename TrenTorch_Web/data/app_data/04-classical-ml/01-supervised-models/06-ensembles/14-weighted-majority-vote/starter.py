import numpy as np


def weighted_majority_vote(predictions: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """
    Combine m classifiers' integer predictions (shape (m, n)) with weights
    (length m). Returns the winning label per sample, ties to the smaller
    label. Raises ValueError for negative weights, zero total weight, or a
    shape mismatch.
    """
    pass
