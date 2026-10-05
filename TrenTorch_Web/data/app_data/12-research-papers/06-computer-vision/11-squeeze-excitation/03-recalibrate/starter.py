import numpy as np


def recalibrate(x, s):
    """
    x: feature map, shape (H, W, C)
    s: per-channel gates, shape (C,)

    Returns:
        The feature map with each channel multiplied by its gate, shape (H, W, C).
    """
    # TODO: Multiply every channel by its gate, broadcasting over space (see Theory).
    pass
