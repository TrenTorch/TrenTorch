import numpy as np


def nonrecurrent_dropout(h, mask, p):
    """
    h: activations on a non-recurrent connection (input to the next layer or the output)
    mask: keep mask with the same shape, 1 where kept
    p: drop probability

    Returns:
        The inverted-dropout output h * mask / (1 - p). The recurrent connection is not passed through this.
    """
    # TODO: Apply the keep mask and rescale by 1 / (1 - p) (see Theory).
    pass
