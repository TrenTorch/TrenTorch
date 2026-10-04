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
    pass
