import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_multi_filter = load_solution("07-vision/01-convolutions/05-multiple-output-filters").conv2d_multi_filter
relu_forward = load_solution("02-deep-learning-core/02-activations/01-relu").relu_forward
max_pool2d = load_solution("07-vision/02-pooling/01-max-pooling").max_pool2d


def cnn_block(image: np.ndarray, kernel: np.ndarray, pool_size: int = 2) -> np.ndarray:
    """
    image:  shape (C_in, H, W)
    kernel: shape (C_out, C_in, kH, kW)
    pool_size: max-pooling window (and stride, non-overlapping)

    Returns the block's output after conv -> ReLU -> max pool, in that
    order.
    """
    # TODO: Chain three already-built pieces in sequence: convolve
    # (05-multiple-output-filters), apply ReLU elementwise, then
    # max-pool the activated result (01-max-pooling). No new math here
    # -- this question is entirely about the wiring.
    pass
