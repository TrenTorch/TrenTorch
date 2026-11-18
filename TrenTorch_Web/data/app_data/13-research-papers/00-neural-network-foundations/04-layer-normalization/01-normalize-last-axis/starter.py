import numpy as np


def normalize_last_axis(x, eps=1e-5):
    """
    x: activations, shape (..., D)
    eps: small constant for numerical stability

    Returns:
        x normalized to zero mean and unit variance over the last axis,
        independently for each example.
    """
    # TODO: Normalize each row over its feature axis (see Theory).
    pass
