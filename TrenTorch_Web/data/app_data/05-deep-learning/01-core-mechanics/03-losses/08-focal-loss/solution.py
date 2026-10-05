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
    if logits.shape != labels.shape:
        raise ValueError("logits and labels must have the same shape")

    if gamma < 0:
        raise ValueError("gamma must be non-negative")

    probs = 1.0 / (1.0 + np.exp(-logits))

    p_t = np.where(labels == 1, probs, 1.0 - probs)

    ce_loss = -np.log(np.clip(p_t, 1e-7, 1.0 - 1e-7))

    focal_weight = (1.0 - p_t) ** gamma

    loss = np.mean(focal_weight * ce_loss)

    return loss
