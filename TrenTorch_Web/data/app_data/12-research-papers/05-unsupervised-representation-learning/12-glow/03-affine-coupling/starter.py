import numpy as np


def affine_coupling_forward(xa, xb, s, t):
    """
    xa: the half of the features passed through unchanged
    xb: the half transformed by the affine map
    s: log-scale computed from xa by a neural network, same shape as xb
    t: shift computed from xa by a neural network, same shape as xb

    Returns:
        (ya, yb) with ya = xa and yb = xb * exp(s) + t.
    """
    # TODO: Keep the first half and apply the scale and shift to the second half (see Theory).
    pass
