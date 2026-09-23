import numpy as np


def conv2d_with_stride(image: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    image:  shape (H, W)
    kernel: shape (kH, kW)
    stride: how many pixels to move the kernel between output positions

    Returns the strided, valid (no padding) convolution output, shape
    ((H - kH) // stride + 1, (W - kW) // stride + 1).
    """
    # TODO: Same sliding-window computation as 01-single-filter-conv2d,
    # but step the top-left corner by `stride` pixels each time instead
    # of by 1 -- multiply the output index by stride to get the real
    # image position.
    pass
