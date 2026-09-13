import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_single_filter = load_solution("07-vision/01-convolutions/01-single-filter-conv2d").conv2d_single_filter


def conv2d_multi_channel(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    C_in, H, W = image.shape
    _, kH, kW = kernel.shape
    output = np.zeros((H - kH + 1, W - kW + 1), dtype=image.dtype)
    for c in range(C_in):
        output += conv2d_single_filter(image[c], kernel[c])
    return output
