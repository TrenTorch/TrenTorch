import numpy as np


def general_score(h_t, W, h_s):
    """
    h_t: decoder hidden state, shape (d_t,)
    W: learned matrix, shape (d_t, d_s)
    h_s: encoder hidden state, shape (d_s,)

    Returns:
        The score h_t^T W h_s, as a float.
    """
    # TODO: Compute the bilinear score h_t W h_s (see Theory).
    pass
