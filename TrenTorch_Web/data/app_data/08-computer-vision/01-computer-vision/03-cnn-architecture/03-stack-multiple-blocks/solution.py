
import numpy as np

from _load import load_solution

cnn_block = load_solution("vision-cnn-one-block").cnn_block


def stack_cnn_blocks(image: np.ndarray, kernels: list, pool_size: int = 2) -> np.ndarray:
    x = image
    for kernel in kernels:
        x = cnn_block(x, kernel, pool_size=pool_size)
    return x
