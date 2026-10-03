
import numpy as np

from _load import load_solution

pointwise_conv = load_solution("vision-modern-pointwise-conv").pointwise_conv


def nearest_upsample_2x(x: np.ndarray) -> np.ndarray:
    return x.repeat(2, axis=1).repeat(2, axis=2)


def fpn_merge(higher_res: np.ndarray, lower_res: np.ndarray, lateral_kernel: np.ndarray) -> np.ndarray:
    lateral = pointwise_conv(higher_res, lateral_kernel)
    upsampled = nearest_upsample_2x(lower_res)
    return lateral + upsampled
