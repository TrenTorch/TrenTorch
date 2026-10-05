import numpy as np


def local_response_norm(x, k=2.0, alpha=1e-4, beta=0.75, n=5):
    """Apply local response normalization.

    Args:
        x: Input array, shape (N, C, H, W).
        k: Constant bias.
        alpha: Scaling constant for neighborhood sum.
        beta: Exponent constant.
        n: Neighborhood size (number of channels to consider).

    Returns:
        Normalized output, same shape as x.

    Raises:
        ValueError: If parameters are invalid.
    """
    pass
