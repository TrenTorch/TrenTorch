import numpy as np


def split_heads(x, h):
    """
    x: a sequence of vectors, shape (T, d), with d divisible by h
    h: number of attention heads

    Returns:
        An array of shape (h, T, d // h): each head gets its own slice of the features.
    """
    # TODO: Reshape to (T, h, d // h) and move the head axis to the front (see Theory).
    pass
