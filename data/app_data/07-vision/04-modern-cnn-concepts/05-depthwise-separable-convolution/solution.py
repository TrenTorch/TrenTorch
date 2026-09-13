import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_single_filter = load_solution("07-vision/01-convolutions/01-single-filter-conv2d").conv2d_single_filter
pointwise_conv = load_solution("07-vision/04-modern-cnn-concepts/03-1x1-convolution").pointwise_conv


def depthwise_separable_conv2d(
    x: np.ndarray, depthwise_kernel: np.ndarray, pointwise_kernel: np.ndarray
) -> np.ndarray:
    C_in = x.shape[0]
    depth_outs = [conv2d_single_filter(x[c], depthwise_kernel[c, 0]) for c in range(C_in)]
    depth_out = np.stack(depth_outs)
    return pointwise_conv(depth_out, pointwise_kernel)
