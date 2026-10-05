import numpy as np


def nesterov_step(param, grad, velocity, lr, momentum):
    """Apply one Nesterov momentum update.

    The gradient is evaluated at the current parameter. The function
    computes a new velocity and uses that velocity in the parameter
    update.

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
    pass
