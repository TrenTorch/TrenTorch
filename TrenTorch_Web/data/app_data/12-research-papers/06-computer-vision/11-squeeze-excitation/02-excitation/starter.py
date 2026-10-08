import numpy as np


def excitation(s, W1, W2):
    """
    s: channel summary from the squeeze step, shape (C,)
    W1: first projection, shape (C // r, C)
    W2: second projection, shape (C, C // r)

    Returns:
        Per-channel gates sigmoid(W2 relu(W1 s)), shape (C,), with values in (0, 1).
    """
    # TODO: Apply the bottleneck with ReLU, then the sigmoid gate (see Theory).
    pass
