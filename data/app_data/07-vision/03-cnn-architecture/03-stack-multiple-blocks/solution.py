import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

cnn_block = load_solution("07-vision/03-cnn-architecture/02-one-cnn-block").cnn_block


def stack_cnn_blocks(image: np.ndarray, kernels: list, pool_size: int = 2) -> np.ndarray:
    x = image
    for kernel in kernels:
        x = cnn_block(x, kernel, pool_size=pool_size)
    return x
