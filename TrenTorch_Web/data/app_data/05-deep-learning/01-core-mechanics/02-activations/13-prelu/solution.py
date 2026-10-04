import numpy as np


def prelu(x, alpha):
    """Compute PReLU (Parametric ReLU) activation.

    Args:
        x: Input array of any shape.
        alpha: Scalar or array-like with same shape as x.
               Slope for negative inputs.

    Returns:
        Output array with same shape as x.
    """
    return np.where(x < 0, alpha * x, x)
