import numpy as np


def highway_gate(x, W, b):
    """
    x: input activations, shape (N, D)
    W: gate weight matrix, shape (D, D)
    b: gate bias, shape (D,)

    Returns:
        The transform gate t = sigmoid(x @ W.T + b), shape (N, D), with values in (0, 1).
    """
    # TODO: Compute the affine map and apply a sigmoid (see Theory).
    pass
