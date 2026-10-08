import numpy as np


def context_vector(weights, H):
    """
    weights: attention weights, shape (T,), summing to 1
    H: encoder states, shape (T, d)

    Returns:
        The weighted average of the encoder states, shape (d,).
    """
    # TODO: Take the weighted sum of the encoder states (see Theory).
    pass
