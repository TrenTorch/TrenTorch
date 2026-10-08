import numpy as np


def additive_scores(s, H, W, U, v):
    """
    s: decoder state, shape (d_s,)
    H: encoder states, shape (T, d_h)
    W: shape (d_a, d_s), U: shape (d_a, d_h), v: shape (d_a,)

    Returns:
        Alignment scores e_j = v . tanh(W s + U h_j), shape (T,).
    """
    # TODO: Compute the additive score for every encoder state (see Theory).
    pass
