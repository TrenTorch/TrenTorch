import numpy as np


def actnorm_forward(x, scale, bias):
    """
    x: activations, shape (..., C) with channels last
    scale: per-channel scale, shape (C,)
    bias: per-channel bias, shape (C,)

    Returns:
        The affine-normalized activations (x + bias) * scale.
    """
    # TODO: Add the per-channel bias and multiply by the per-channel scale (see Theory).
    pass
