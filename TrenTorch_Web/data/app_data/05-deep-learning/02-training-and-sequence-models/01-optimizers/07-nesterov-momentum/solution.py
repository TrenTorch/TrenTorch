import numpy as np


def nesterov_step(param, grad, velocity, lr, momentum):
    """Apply one Nesterov momentum update.

    Args:
        param: Parameter array.
        grad: Gradient array with the same shape as param.
        velocity: Current velocity array with the same shape as param.
        lr: Learning rate.
        momentum: Momentum coefficient in [0, 1).

    Returns:
        A tuple (new_param, new_velocity).

    Raises:
        ValueError: If input shapes do not match or momentum is outside
            the range [0, 1).
    """
    if param.shape != grad.shape or param.shape != velocity.shape:
        raise ValueError(
            "param, grad, and velocity must have the same shape"
        )

    if not 0 <= momentum < 1:
        raise ValueError("momentum must be in [0, 1)")

    v_new = momentum * velocity + grad
    param_new = param - lr * (grad + momentum * v_new)

    return param_new, v_new
