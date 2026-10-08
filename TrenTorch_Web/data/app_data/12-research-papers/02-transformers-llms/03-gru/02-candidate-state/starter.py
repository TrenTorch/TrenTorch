import numpy as np


def gru_candidate(x, h, r, W, U):
    """
    x: input at this step, shape (d_x,)
    h: previous hidden state, shape (d_h,)
    r: reset gate, shape (d_h,), values in (0, 1)
    W: shape (d_h, d_x), U: shape (d_h, d_h)

    Returns:
        The candidate state tanh(W x + U (r * h)), shape (d_h,).
    """
    # TODO: Gate the previous state by r, then apply tanh (see Theory).
    pass
