import numpy as np


def instance_norm(x, gamma, beta, eps=1e-5):
    """Apply instance normalization.

    Args:
        x: Input array, shape (N, C, H, W) or (N, C).
        gamma: Scale parameter, shape (C,).
        beta: Shift parameter, shape (C,).
        eps: Numerical stability constant.

    Returns:
        Normalized output, same shape as x.

    Raises:
        ValueError: If gamma/beta shapes don't match C.
    """
    pass
