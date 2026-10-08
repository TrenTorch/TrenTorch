import numpy as np


def skip_concat(enc, dec):
    """
    enc: encoder features, shape (H, W, C1), already cropped to match
    dec: decoder features, shape (H, W, C2)

    Returns:
        The features joined along the channel axis, shape (H, W, C1 + C2).
    """
    # TODO: Concatenate the two maps along the last axis (see Theory).
    pass
