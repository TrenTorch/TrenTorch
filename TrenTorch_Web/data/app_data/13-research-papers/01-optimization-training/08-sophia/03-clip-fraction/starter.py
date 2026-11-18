import numpy as np


def clip_fraction(ratios):
    """
    ratios: unclipped per-coordinate ratios m / max(gamma * h, eps)

    Returns:
        The fraction of coordinates whose magnitude is at least one, which get clipped.
    """
    # TODO: Count the entries with absolute value at least one and divide by the total (see Theory).
    pass
