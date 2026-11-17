import numpy as np


def upsample_nearest(x, f):
    """
    x: feature map, shape (H, W, ...)
    f: integer upsampling factor

    Returns:
        A map of shape (H * f, W * f, ...) where each value is repeated f times along each spatial axis.
    """
    # TODO: Repeat each value f times along both spatial axes (see Theory).
    pass
