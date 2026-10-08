import numpy as np


def softmax_temperature(logits, T):
    """
    logits: raw class scores, shape (..., C)
    T: temperature (positive); T = 1 is the ordinary softmax

    Returns:
        softmax(logits / T), computed over the last axis.
    """
    # TODO: Divide the logits by T and apply a stable softmax (see Theory).
    pass
