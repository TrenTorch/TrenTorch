import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

pointwise_conv = load_solution("07-vision/04-modern-cnn-concepts/03-1x1-convolution").pointwise_conv


def nearest_upsample_2x(x: np.ndarray) -> np.ndarray:
    """
    x: shape (C, H, W)
    Returns shape (C, 2H, 2W): every pixel repeated into a 2x2 block.
    """
    # TODO: repeat every element along the H axis twice, then along the
    # W axis twice (np.ndarray.repeat(n, axis=...) is exactly this).
    pass


def fpn_merge(higher_res: np.ndarray, lower_res: np.ndarray, lateral_kernel: np.ndarray) -> np.ndarray:
    """
    higher_res: shape (C_high, 2H, 2W) -- an early, high-resolution,
        low-level backbone feature map
    lower_res: shape (C_low, H, W) -- a later, lower-resolution,
        high-level backbone feature map (exactly half the spatial size
        of higher_res)
    lateral_kernel: shape (C_low, C_high, 1, 1) -- projects higher_res's
        channel count to match lower_res's, so the two can be added

    A Feature Pyramid Network combines information from multiple scales:
    an early layer's high-resolution-but-low-level features are merged
    with a later layer's low-resolution-but-high-level (semantically
    richer) features, giving a detector access to both fine spatial
    detail and rich semantic content at every scale.
    """
    # TODO: run a 1x1 "lateral" convolution (pointwise_conv) on
    # higher_res with lateral_kernel to match lower_res's channel count,
    # upsample lower_res by 2x with nearest_upsample_2x to match
    # higher_res's spatial size, then add the two together.
    pass
