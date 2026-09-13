import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_single_filter = load_solution("07-vision/01-convolutions/01-single-filter-conv2d").conv2d_single_filter


def conv2d_with_padding(image: np.ndarray, kernel: np.ndarray, padding: str = "valid") -> np.ndarray:
    """
    image:  shape (H, W)
    kernel: shape (kH, kW), both dimensions odd
    padding: "valid" (no padding) or "same" (output same H, W as input)

    Returns the convolution output.
    """
    # TODO: "valid" is just 01-single-filter-conv2d unchanged. "same"
    # zero-pads image by (k-1)//2 on each side per axis before
    # convolving, so the output comes out the same size as the input.
    pass
