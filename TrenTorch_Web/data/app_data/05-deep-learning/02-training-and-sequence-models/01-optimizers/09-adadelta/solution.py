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
    if (
        param.shape != grad.shape
        or param.shape != square_avg.shape
        or param.shape != acc_delta.shape
    ):
        raise ValueError(
            "param, grad, square_avg, and acc_delta "
            "must have the same shape"
        )

    if lr <= 0:
        raise ValueError("lr must be positive")

    if not 0 <= rho < 1:
        raise ValueError("rho must be in [0, 1)")

    if eps <= 0:
        raise ValueError("eps must be positive")

    square_avg_new = (
        rho * square_avg
        + (1 - rho) * grad * grad
    )

    delta = (
        np.sqrt(acc_delta + eps)
        / np.sqrt(square_avg_new + eps)
        * grad
    )

    param_new = param - lr * delta

    acc_delta_new = (
        rho * acc_delta
        + (1 - rho) * delta * delta
    )

    return param_new, square_avg_new, acc_delta_new
