import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_single_filter = load_solution("07-vision/01-convolutions/01-single-filter-conv2d").conv2d_single_filter


def conv2d_multi_channel(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    image:  shape (C_in, H, W)
    kernel: shape (C_in, kH, kW) -- one 2D filter per input channel

    Returns the single-channel output, shape (H - kH + 1, W - kW + 1):
    the sum, across channels, of each channel's own 2D convolution.
    """
    # TODO: Convolve each input channel with its own 2D slice of the
    # kernel (reuse 01-single-filter-conv2d's conv2d_single_filter),
    # then sum the C_in results into one output.
    pass
