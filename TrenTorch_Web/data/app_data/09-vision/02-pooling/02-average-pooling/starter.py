import numpy as np


def avg_pool2d(image: np.ndarray, kernel_size: int, stride: int | None = None) -> np.ndarray:
    """
    image: shape (C, H, W)
    kernel_size: pooling window size
    stride: step between windows; defaults to kernel_size (non-overlapping)

    Returns shape (C, out_h, out_w), the mean over each window,
    per channel independently.
    """
    # TODO: Same sliding-window structure as 01-max-pooling, but average
    # the window instead of taking its max.
    pass
