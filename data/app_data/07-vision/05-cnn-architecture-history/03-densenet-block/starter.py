import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_multi_filter = load_solution("07-vision/01-convolutions/05-multiple-output-filters").conv2d_multi_filter
relu_forward = load_solution("02-deep-learning-core/02-activations/01-relu").relu_forward


def dense_block(x: np.ndarray, kernels: list) -> np.ndarray:
    """
    x: shape (C, H, W)
    kernels: list of 3x3 kernels. kernels[i] must accept as many input
        channels as the CURRENT running feature count (C plus every
        previous layer's output channels), since DenseNet feeds each
        layer ALL previous feature maps concatenated together.

    Unlike a residual connection (which ADDS a layer's input to its
    output), a dense connection CONCATENATES every previous layer's
    output onto a growing feature stack, so layer i sees everything
    every earlier layer ever produced, not just an additive combination
    of it.
    """
    # TODO: start `features = x`. For each kernel: same-pad `features` by
    # 1 pixel, run conv2d_multi_filter + relu_forward to get this layer's
    # new output, then np.concatenate the new output onto `features`
    # along the channel axis (axis=0) so the NEXT layer sees everything
    # produced so far. Return the final, fully-grown `features`.
    pass
