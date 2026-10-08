import numpy as np


def trust_ratio(w, g, eta, wd):
    """
    w: a layer's weights; g: its gradient; eta: trust coefficient; wd: weight decay

    Returns:
        The local learning-rate multiplier eta * ||w|| / (||g|| + wd * ||w||).
    """
    # TODO: Compare the weight norm to the gradient norm plus decay (see Theory).
    pass
