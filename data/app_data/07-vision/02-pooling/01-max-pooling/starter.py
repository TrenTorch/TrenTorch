import numpy as np


def max_pool2d(image: np.ndarray, kernel_size: int, stride: int | None = None) -> np.ndarray:
    """
    image: shape (C, H, W)
    kernel_size: pooling window size
    stride: step between windows; defaults to kernel_size (non-overlapping)

    Returns shape (C, out_h, out_w), the max over each window,
    per channel independently.
    """
    # TODO: Slide a (kernel_size, kernel_size) window with the given
    # stride, per channel, and take the max over each window -- same
    # sliding-window structure as 01-convolutions, but max instead of
    # a weighted sum, and no kernel weights at all.
    pass
