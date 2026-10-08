import math

import numpy as np


def magnitude_mask(w, keep_fraction):
    """
    w: weight array of any shape
    keep_fraction: fraction of weights to keep, in [0, 1]

    Returns:
        A boolean mask of the same shape as w, True for the ceil(keep_fraction * size)
        weights with the largest absolute value.
    """
    # TODO: Keep the largest-magnitude weights and return the mask (see Theory).
    pass
