import numpy as np


def bce_with_logits_loss(z: np.ndarray, y: np.ndarray) -> float:
    """
    Numerically stable BCE computed directly from raw logits z,
    without ever computing a separate sigmoid(z) probability array.
    """
    # TODO: Implement the fused, numerically-stable formula from Theory --
    # max(z, 0) - z*y + log(1 + exp(-|z|)) -- using np.log1p and
    # np.exp(-np.abs(z)) so the exponent argument is never positive.
    pass
