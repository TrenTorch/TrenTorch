import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_multi_filter = load_solution("07-vision/01-convolutions/05-multiple-output-filters").conv2d_multi_filter
relu_forward = load_solution("02-deep-learning-core/02-activations/01-relu").relu_forward


def dense_block(x: np.ndarray, kernels: list) -> np.ndarray:
    features = x
    for kernel in kernels:
        padded = np.pad(features, ((0, 0), (1, 1), (1, 1)))
        new_layer = relu_forward(conv2d_multi_filter(padded, kernel))
        features = np.concatenate([features, new_layer], axis=0)
    return features
