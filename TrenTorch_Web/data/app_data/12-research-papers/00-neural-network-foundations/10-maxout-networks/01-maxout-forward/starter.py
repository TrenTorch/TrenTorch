import numpy as np


def maxout_forward(x, W, b, k):
    """
    x: inputs, shape (N, D)
    W: weights for all k pieces of all output units, shape (out * k, D)
    b: biases, shape (out * k,)
    k: number of linear pieces per output unit

    Returns:
        The maxout output, shape (N, out): for each unit, the max over its k pieces.
    """
    # TODO: Compute all linear pieces, group them into k per unit, and take the max (see Theory).
    pass
