import numpy as np


def batch_norm2d(x: np.ndarray, gamma: np.ndarray, beta: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    """
    x: shape (N, C, H, W) -- a batch of feature maps
    gamma: shape (C,) -- learned per-channel scale
    beta: shape (C,) -- learned per-channel shift

    Normalize each channel using the mean and variance computed over the
    batch, height and width dimensions (N, H, W) for that channel, then
    apply the learned scale and shift.
    """
    # TODO: compute per-channel mean and variance over axes (0, 2, 3),
    # normalize x, then scale by gamma and shift by beta (both reshaped
    # to broadcast against (N, C, H, W)).
    pass
