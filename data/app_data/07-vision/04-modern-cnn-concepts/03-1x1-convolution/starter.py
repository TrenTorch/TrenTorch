import numpy as np


def pointwise_conv(x: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    x: shape (C_in, H, W)
    kernel: shape (C_out, C_in, 1, 1) -- a 1x1 convolution kernel

    A 1x1 convolution never mixes information across spatial positions --
    every output pixel only depends on the C_in input values at that exact
    (h, w) location. That makes it equivalent to applying the same
    (C_out, C_in) linear map independently to every pixel's channel
    vector, so it can be implemented as a single reshape + matmul instead
    of any loop over spatial positions.
    """
    # TODO: squeeze kernel down to a (C_out, C_in) weight matrix, reshape
    # x to (C_in, H*W), matrix-multiply, then reshape the result back to
    # (C_out, H, W).
    pass
