import numpy as np


def highway_layer(x, W_h, b_h, W_t, b_t):
    """
    x: input activations, shape (N, D)
    W_h, b_h: weights and bias of the transform H(x) = tanh(x W_h^T + b_h)
    W_t, b_t: weights and bias of the gate T(x) = sigmoid(x W_t^T + b_t)

    Returns:
        y = H(x) * T(x) + x * (1 - T(x)), shape (N, D).
    """
    # TODO: Compute the transform and gate, then blend them with the input (see Theory).
    pass
