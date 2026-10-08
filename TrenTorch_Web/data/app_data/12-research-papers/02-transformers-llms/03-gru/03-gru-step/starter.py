import numpy as np


def gru_step(x, h, Wz, Uz, Wr, Ur, W, U):
    """
    x: input at this step, shape (d_x,)
    h: previous hidden state, shape (d_h,)
    Wz, Wr, W: input weights, shape (d_h, d_x)
    Uz, Ur, U: recurrent weights, shape (d_h, d_h)

    Returns:
        The new hidden state (1 - z) * h + z * h_tilde, shape (d_h,).
    """
    # TODO: Compute the update gate, reset gate and candidate, then blend (see Theory).
    pass
