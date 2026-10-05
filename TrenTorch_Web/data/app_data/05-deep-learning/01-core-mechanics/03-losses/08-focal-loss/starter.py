import numpy as np


def focal_loss(logits, labels, gamma=2.0):
    """Compute focal loss for binary classification.

    Args:
        logits: Predicted logits, same shape as labels.
        labels: Ground truth labels (0 or 1), same shape as logits.
        gamma: Focusing parameter (gamma >= 0).

    Returns:
        Scalar loss value.

    Raises:
        ValueError: If shapes don't match or gamma < 0.
    """
    pass
