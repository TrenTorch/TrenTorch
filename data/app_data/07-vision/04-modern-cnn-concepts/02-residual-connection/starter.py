import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_multi_filter = load_solution("07-vision/01-convolutions/05-multiple-output-filters").conv2d_multi_filter
relu_forward = load_solution("02-deep-learning-core/02-activations/01-relu").relu_forward


def residual_block(x: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    x: shape (C, H, W) -- a single image / feature map
    kernel: shape (C, C, 3, 3) -- same in/out channel count as x

    Run x through a 3x3 "same"-padded convolution (so the conv output has
    the exact same shape as x), add x back to the result (the skip
    connection), then apply ReLU.
    """
    # TODO: pad x by 1 on each side of H and W (so a 3x3 conv preserves
    # spatial size), run conv2d_multi_filter on the padded input, add the
    # ORIGINAL (unpadded) x to the conv output, then relu_forward the sum.
    pass
