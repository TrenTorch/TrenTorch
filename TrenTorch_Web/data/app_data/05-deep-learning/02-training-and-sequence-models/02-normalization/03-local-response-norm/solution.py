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
    if k <= 0 or alpha <= 0 or beta <= 0 or n <= 0:
        raise ValueError("k, alpha, beta, n must be positive")

    n_half = n // 2
    x_squared = x ** 2
    result = np.zeros_like(x)

    for c in range(x.shape[1]):
        c_start = max(0, c - n_half)
        c_end = min(x.shape[1], c + n_half + 1)
        neighborhood_sum = np.sum(x_squared[:, c_start:c_end, :, :], axis=1, keepdims=True)
        norm_factor = (k + alpha * neighborhood_sum) ** beta
        result[:, c, :, :] = x[:, c, :, :] / norm_factor[:, 0, :, :]

    return result
