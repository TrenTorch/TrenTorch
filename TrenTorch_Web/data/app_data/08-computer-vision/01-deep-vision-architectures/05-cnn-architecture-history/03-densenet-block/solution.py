
import numpy as np

from _load import load_solution

conv2d_multi_filter = load_solution("vision-conv-multi-filter").conv2d_multi_filter
relu_forward = load_solution("dl-activation-relu").relu_forward


def dense_block(x: np.ndarray, kernels: list) -> np.ndarray:
    features = x
    for kernel in kernels:
        padded = np.pad(features, ((0, 0), (1, 1), (1, 1)))
        new_layer = relu_forward(conv2d_multi_filter(padded, kernel))
        features = np.concatenate([features, new_layer], axis=0)
    return features
