import numpy as np


def gru_update_gate(x, h, Wz, Uz):
    """
    x: input at this step, shape (d_x,)
    h: previous hidden state, shape (d_h,)
    Wz: shape (d_h, d_x), Uz: shape (d_h, d_h)

    Returns:
        The update gate z = sigmoid(Wz x + Uz h), shape (d_h,), values in (0, 1).
    """
    # TODO: Apply the sigmoid to the affine map of x and h (see Theory).
    pass
