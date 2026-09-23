import numpy as np


def conv2d_im2col(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    image:  shape (C_in, H, W)
    kernel: shape (C_out, C_in, kH, kW)

    Same contract and output as 05-multiple-output-filters, but computed
    via im2col: gather every sliding-window patch into one big matrix,
    then compute all output positions and all filters with a single
    matrix multiply instead of nested loops.
    """
    # TODO: Use np.lib.stride_tricks.sliding_window_view(image, (kH, kW),
    # axis=(1, 2)) to get every patch without a Python loop, reshape
    # into a (out_h*out_w, C_in*kH*kW) matrix, flatten kernel the same
    # way, and multiply.
    pass
