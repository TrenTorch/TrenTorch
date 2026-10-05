import numpy as np


def adagrad_step(param, grad, accum, lr, eps):
    """Apply one Adagrad optimization step.

    The accumulator stores the element-wise sum of squared gradients.
    It starts at zeros and is updated before computing the parameter
    update.

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
    pass
