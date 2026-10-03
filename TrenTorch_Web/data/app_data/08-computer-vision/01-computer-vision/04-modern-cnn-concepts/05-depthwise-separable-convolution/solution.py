
import numpy as np

from _load import load_solution

conv2d_single_filter = load_solution("vision-conv-single-filter").conv2d_single_filter
pointwise_conv = load_solution("vision-modern-pointwise-conv").pointwise_conv


def depthwise_separable_conv2d(
    x: np.ndarray, depthwise_kernel: np.ndarray, pointwise_kernel: np.ndarray
) -> np.ndarray:
    C_in = x.shape[0]
    depth_outs = [conv2d_single_filter(x[c], depthwise_kernel[c, 0]) for c in range(C_in)]
    depth_out = np.stack(depth_outs)
    return pointwise_conv(depth_out, pointwise_kernel)
