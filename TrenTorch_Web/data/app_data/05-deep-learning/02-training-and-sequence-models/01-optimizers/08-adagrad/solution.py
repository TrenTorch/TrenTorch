import numpy as np


def adagrad_step(param, grad, accum, lr, eps):
    """Apply one Adagrad optimization step.

    Args:
        param: Parameter array.
        grad: Gradient array with the same shape as param.
        accum: Accumulated squared-gradient array with the same shape
            as param.
        lr: Positive learning rate.
        eps: Positive numerical stability constant.

    Returns:
        A tuple (new_param, new_accum).

    Raises:
        ValueError: If the input shapes do not match, or if lr or eps
            is not positive.
    """
    if param.shape != grad.shape or param.shape != accum.shape:
        raise ValueError(
            "param, grad, and accum must have the same shape"
        )

    if lr <= 0:
        raise ValueError("lr must be positive")

    if eps <= 0:
        raise ValueError("eps must be positive")

    accum_new = accum + grad * grad
    param_new = param - lr * grad / (
        np.sqrt(accum_new) + eps
    )

    return param_new, accum_new
