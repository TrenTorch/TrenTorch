import numpy as np


def selu(x):
    """Compute SELU activation with self-normalizing properties.

    Args:
        x: Input array of any shape.

    Returns:
        Output array with same shape as x.
    """
    LAMBDA = 1.0507
    ALPHA = 1.6733
    return LAMBDA * np.where(
        x < 0,
        ALPHA * (np.exp(x) - 1),
        x,
    )
