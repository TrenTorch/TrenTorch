import numpy as np


def conv2d_single_filter(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    image:  shape (H, W)
    kernel: shape (kH, kW)

    Returns the valid (no padding) cross-correlation of image with
    kernel, shape (H - kH + 1, W - kW + 1).
    """
    # TODO: Implement 2D convolution from Theory. For every valid
    # top-left position, elementwise-multiply the image patch under the
    # kernel and sum -- no kernel flipping (this is cross-correlation,
    # which is what every deep learning framework actually calls "conv").
    pass
