
import numpy as np

from _load import load_solution

conv2d_single_filter = load_solution("vision-conv-single-filter").conv2d_single_filter
pointwise_conv = load_solution("vision-modern-pointwise-conv").pointwise_conv


def depthwise_separable_conv2d(
    x: np.ndarray, depthwise_kernel: np.ndarray, pointwise_kernel: np.ndarray
) -> np.ndarray:
    """
    x: shape (C_in, H, W)
    depthwise_kernel: shape (C_in, 1, kH, kW) -- one independent kH x kW
        filter per input channel; channels are NEVER mixed at this stage
    pointwise_kernel: shape (C_out, C_in, 1, 1) -- a 1x1 conv that mixes
        channels together afterward

    A regular (C_out, C_in, kH, kW) convolution does spatial filtering and
    channel mixing in one expensive step. Depthwise-separable convolution
    splits that into two much cheaper steps: first filter each channel
    independently (no channel mixing), then mix channels with a 1x1 conv
    (no spatial filtering).
    """
    # TODO: for each input channel c, run conv2d_single_filter(x[c],
    # depthwise_kernel[c, 0]) to get that channel's filtered output (no
    # channel mixing yet). Stack these C_in results back into one
    # (C_in, H', W') array, then run pointwise_conv on that with
    # pointwise_kernel to mix channels into the final (C_out, H', W').
    pass
