import numpy as np


def adadelta_step(
    param,
    grad,
    square_avg,
    acc_delta,
    lr,
    rho,
    eps,
):
    """Apply one Adadelta optimization step.

    The function maintains an exponential moving average of squared
    gradients and an exponential moving average of squared updates.

    Args:
        param: Parameter array.
        grad: Gradient array with the same shape as param.
        square_avg: Moving average of squared gradients.
        acc_delta: Moving average of squared parameter updates.
        lr: Positive learning rate.
        rho: Decay factor in [0, 1).
        eps: Positive numerical stability constant.

    Returns:
        A tuple (new_param, new_square_avg, new_acc_delta).

    Raises:
        ValueError: If input shapes do not match, lr is not positive,
            rho is outside [0, 1), or eps is not positive.
    """
    pass
