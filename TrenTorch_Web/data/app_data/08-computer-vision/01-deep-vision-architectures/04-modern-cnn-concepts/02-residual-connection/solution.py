
import numpy as np

from _load import load_solution

conv2d_multi_filter = load_solution("vision-conv-multi-filter").conv2d_multi_filter
relu_forward = load_solution("dl-core-relu").relu_forward


def residual_block(x: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    padded = np.pad(x, ((0, 0), (1, 1), (1, 1)))
    conv_out = conv2d_multi_filter(padded, kernel)
    return relu_forward(x + conv_out)
