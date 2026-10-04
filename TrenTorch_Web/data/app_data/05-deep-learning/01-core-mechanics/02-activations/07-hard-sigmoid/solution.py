import numpy as np


def hard_sigmoid(x):
    """Compute hard sigmoid activation.

    Args:
        x: Input array of any shape.

    Returns:
        Output array with same shape as x, values in [0, 1].
    """
    return (np.clip(x, -2.5, 2.5) + 2.5) / 5.0
