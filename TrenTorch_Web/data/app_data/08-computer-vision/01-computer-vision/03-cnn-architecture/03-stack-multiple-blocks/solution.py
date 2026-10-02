import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

cnn_block = load_solution("08-computer-vision/01-computer-vision/03-cnn-architecture/02-one-cnn-block").cnn_block


def stack_cnn_blocks(image: np.ndarray, kernels: list, pool_size: int = 2) -> np.ndarray:
    x = image
    for kernel in kernels:
        x = cnn_block(x, kernel, pool_size=pool_size)
    return x
