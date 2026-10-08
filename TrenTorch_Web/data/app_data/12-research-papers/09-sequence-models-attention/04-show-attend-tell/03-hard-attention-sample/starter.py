import numpy as np


def sample_hard_attention(alpha, rng):
    """
    alpha: attention distribution over locations, shape (L,), summing to 1
    rng: a NumPy Generator

    Returns:
        A location index sampled from alpha, as a Python int.
    """
    # TODO: Draw one location index from the attention distribution (see Theory).
    pass
