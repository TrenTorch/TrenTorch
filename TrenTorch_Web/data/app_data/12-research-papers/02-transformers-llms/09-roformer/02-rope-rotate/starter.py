import numpy as np


def rope_rotate(x, pos, base=10000.0):
    """
    x: a vector of even length d
    pos: the token position (number)
    base: the frequency base

    Returns:
        x with each consecutive pair (x[2i], x[2i+1]) rotated by pos * theta_i.
    """
    # TODO: Rotate each feature pair by its position-dependent angle (see Theory).
    pass
