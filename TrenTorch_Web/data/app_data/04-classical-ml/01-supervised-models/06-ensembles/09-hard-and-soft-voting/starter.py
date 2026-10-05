import numpy as np


def hard_vote(predictions: np.ndarray) -> np.ndarray:
    """
    predictions: (n_models, n_samples) integer class labels.

    Returns:
        (n_samples,) majority label per sample; ties go to the smallest label.
    """
    # TODO: Majority vote per column.
    pass


def soft_vote(probabilities: np.ndarray, weights=None) -> np.ndarray:
    """
    probabilities: (n_models, n_samples, n_classes).
    weights: optional (n_models,) non-negative weights.

    Returns:
        (n_samples,) class index with the highest (weighted) mean probability.
    """
    # TODO: Average across models, then argmax over classes.
    pass
