
import numpy as np

from _load import load_solution

conv2d_multi_filter = load_solution("vision-conv-multi-filter").conv2d_multi_filter
relu_forward = load_solution("dl-activation-relu").relu_forward


def vgg_stack(x: np.ndarray, kernels: list) -> np.ndarray:
    for kernel in kernels:
        padded = np.pad(x, ((0, 0), (1, 1), (1, 1)))
        x = relu_forward(conv2d_multi_filter(padded, kernel))
    return x
