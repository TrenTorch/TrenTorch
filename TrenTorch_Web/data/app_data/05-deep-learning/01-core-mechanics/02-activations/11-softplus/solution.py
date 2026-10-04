import numpy as np


def softplus(x, beta=1.0):
    """Compute softplus activation, smooth approximation to ReLU.

    Args:
        x: Input array of any shape.
        beta: Positive steepness parameter.

    Returns:
        Output array with same shape as x, always positive.
    """
    return np.where(
        beta * x > 20.0,
        x,
        (1.0 / beta) * np.log(1.0 + np.exp(beta * x)),
    )
