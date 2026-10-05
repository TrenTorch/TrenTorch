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
    original_shape = x.shape
    n = x.shape[0]
    c = x.shape[1]

    if gamma.shape != (c,) or beta.shape != (c,):
        raise ValueError("gamma and beta must have shape (C,)")

    if len(original_shape) == 4:
        axes = (2, 3)
    else:
        axes = ()

    mean = np.mean(x, axis=axes, keepdims=True)
    var = np.var(x, axis=axes, keepdims=True)

    x_normalized = (x - mean) / np.sqrt(var + eps)

    if len(original_shape) == 4:
        gamma_reshaped = gamma[np.newaxis, :, np.newaxis, np.newaxis]
        beta_reshaped = beta[np.newaxis, :, np.newaxis, np.newaxis]
    else:
        gamma_reshaped = gamma[np.newaxis, :]
        beta_reshaped = beta[np.newaxis, :]

    return x_normalized * gamma_reshaped + beta_reshaped
