import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

cnn_block = load_solution("07-vision/03-cnn-architecture/02-one-cnn-block").cnn_block


def stack_cnn_blocks(image: np.ndarray, kernels: list, pool_size: int = 2) -> np.ndarray:
    """
    image: shape (C_in, H, W)
    kernels: list of kernels, one per block; kernels[i] has shape
        (C_out_i, C_in_i, kH, kW), where C_in_i must match the previous
        block's C_out (or image's own C_in, for the first block)
    pool_size: passed to every block's pooling step

    Returns the final block's output after running image through every
    block in kernels, in order.
    """
    # TODO: Feed image through 02-one-cnn-block's cnn_block once per
    # kernel in the list, each block's output becoming the next block's
    # input. No new math -- this question is purely about chaining.
    pass
