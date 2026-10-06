
import numpy as np

from _load import load_solution

conv2d_multi_filter = load_solution("vision-conv-multi-filter").conv2d_multi_filter
relu_forward = load_solution("dl-activation-relu").relu_forward
max_pool2d = load_solution("vision-pool-max").max_pool2d


def cnn_block(image: np.ndarray, kernel: np.ndarray, pool_size: int = 2) -> np.ndarray:
    conv_out = conv2d_multi_filter(image, kernel)
    activated = relu_forward(conv_out)
    return max_pool2d(activated, kernel_size=pool_size)
