import numpy as np


def dropout_forward(x, keep_mask, p):
    """
    x: activations (NumPy array)
    keep_mask: same shape as x, 1 where a unit is kept, 0 where it is dropped
    p: probability that a unit is dropped (0 <= p < 1)

    Returns:
        The inverted-dropout output: x * keep_mask / (1 - p).
    """
    # TODO: Apply the mask and rescale by 1 / (1 - p) from Theory.
    pass
