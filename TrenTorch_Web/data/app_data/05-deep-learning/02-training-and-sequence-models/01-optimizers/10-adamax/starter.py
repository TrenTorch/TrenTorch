import numpy as np


def adamax_step(
    param,
    grad,
    m,
    u,
    lr,
    beta1,
    beta2,
    eps,
):
    """Apply one Adamax optimization step.

    The function maintains an exponential moving average of gradients
    and tracks the maximum absolute gradient (infinity norm).

    Args:
        param: Parameter array.
        grad: Gradient array with the same shape as param.
        m: First moment (moving average of gradients).
        u: Infinity norm (max absolute gradient seen).
        lr: Positive learning rate.
        beta1: Decay factor for first moment, in [0, 1).
        beta2: Decay factor for infinity norm, in [0, 1).
        eps: Positive numerical stability constant.

    Returns:
        A tuple (new_param, new_m, new_u).

    Raises:
        ValueError: If input shapes do not match, lr is not positive,
            beta1 or beta2 are outside [0, 1), or eps is not positive.
    """
    pass
