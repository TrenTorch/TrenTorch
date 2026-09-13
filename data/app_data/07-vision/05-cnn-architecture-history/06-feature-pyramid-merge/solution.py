import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

pointwise_conv = load_solution("07-vision/04-modern-cnn-concepts/03-1x1-convolution").pointwise_conv


def nearest_upsample_2x(x: np.ndarray) -> np.ndarray:
    return x.repeat(2, axis=1).repeat(2, axis=2)


def fpn_merge(higher_res: np.ndarray, lower_res: np.ndarray, lateral_kernel: np.ndarray) -> np.ndarray:
    lateral = pointwise_conv(higher_res, lateral_kernel)
    upsampled = nearest_upsample_2x(lower_res)
    return lateral + upsampled
