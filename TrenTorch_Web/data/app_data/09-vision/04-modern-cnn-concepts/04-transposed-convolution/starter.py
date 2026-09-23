import numpy as np


def conv_transpose2d(x: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    x: shape (1, H, W) -- a single-channel feature map
    kernel: shape (1, 1, kH, kW)
    stride: how far apart (in the output) each input pixel's contribution
        is placed

    A transposed convolution (sometimes called "deconvolution") does the
    opposite of a normal convolution's shape change: it takes a small
    input and produces a LARGER output, by scattering a scaled copy of
    the kernel into the output at every input pixel's location and
    summing overlaps.

    Output size: out_h = (H - 1) * stride + kH, out_w = (W - 1) * stride + kW.
    """
    # TODO: build a zero output array of the right size, then for every
    # input pixel (i, j), add x[0, i, j] * kernel[0, 0] into the output
    # window starting at (i * stride, j * stride).
    pass
