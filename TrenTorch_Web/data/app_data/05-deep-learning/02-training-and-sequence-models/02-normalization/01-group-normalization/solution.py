import numpy as np


def group_norm(x, num_groups, gamma, beta, eps=1e-5):
    """Apply group normalization.

    Args:
        x: Input array, shape (N, C, H, W) or (N, C).
        num_groups: Number of groups (must divide C).
        gamma: Scale parameter, shape (C,).
        beta: Shift parameter, shape (C,).
        eps: Numerical stability constant.

    Returns:
        Normalized output, same shape as x.

    Raises:
        ValueError: If C % num_groups != 0 or shapes don't match.
    """
    original_shape = x.shape
    n = x.shape[0]
    c = x.shape[1]

    if c % num_groups != 0:
        raise ValueError("num_groups must divide C")

    if gamma.shape != (c,) or beta.shape != (c,):
        raise ValueError("gamma and beta must have shape (C,)")

    x_reshaped = x.reshape(n, num_groups, c // num_groups, -1)

    mean = np.mean(x_reshaped, axis=(2, 3), keepdims=True)
    var = np.var(x_reshaped, axis=(2, 3), keepdims=True)

    x_normalized = (x_reshaped - mean) / np.sqrt(var + eps)

    x_normalized = x_normalized.reshape(original_shape)

    if len(original_shape) == 4:
        gamma_reshaped = gamma[np.newaxis, :, np.newaxis, np.newaxis]
        beta_reshaped = beta[np.newaxis, :, np.newaxis, np.newaxis]
    else:
        gamma_reshaped = gamma[np.newaxis, :]
        beta_reshaped = beta[np.newaxis, :]

    return x_normalized * gamma_reshaped + beta_reshaped
