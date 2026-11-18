import numpy as np


def maxout_argmax(x, W, b, k):
    """
    x: inputs, shape (N, D)
    W: weights, shape (out * k, D)
    b: biases, shape (out * k,)
    k: pieces per output unit

    Returns:
        Integer array of shape (N, out): the index (0 to k-1) of the winning piece
        for each unit and example. Gradients flow only through this piece.
    """
    # TODO: Compute the pieces, group them, and return the argmax of each group (see Theory).
    pass
