import numpy as np


def lamb_update(w, r, lr):
    """
    w: layer weights; r: the Adam-style direction for the layer, including decay
    lr: learning rate

    Returns:
        The weights after one LAMB step, with the direction scaled by the layer's trust ratio.
    """
    # TODO: Scale r by the trust ratio and lr, then subtract from w (see Theory).
    pass
