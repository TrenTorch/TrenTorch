import numpy as np


def softsign(x):
    """Compute softsign activation.

    Args:
        x: Input array of any shape.

    Returns:
        Output array with same shape as x, values in (-1, 1).
    """
    return x / (1.0 + np.abs(x))
