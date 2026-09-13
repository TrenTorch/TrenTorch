import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_multi_filter = load_solution("07-vision/01-convolutions/05-multiple-output-filters").conv2d_multi_filter
relu_forward = load_solution("02-deep-learning-core/02-activations/01-relu").relu_forward


def vgg_stack(x: np.ndarray, kernels: list) -> np.ndarray:
    """
    x: shape (C, H, W)
    kernels: list of 3x3 kernels, each shape (C, C, 3, 3) -- same channel
        count in and out, applied one after another

    VGG's key idea: replace one large-kernel convolution with a STACK of
    small (3x3), "same"-padded 3x3 convolutions. Two stacked 3x3 convs
    see a 5x5 receptive field with a ReLU in between them (one extra
    nonlinearity, and fewer parameters than a single 5x5 conv would use).
    """
    # TODO: for each kernel in kernels (in order), same-pad x by 1 pixel,
    # run conv2d_multi_filter, apply relu_forward, and feed the result
    # into the next iteration as the new x. Return the final x.
    pass
