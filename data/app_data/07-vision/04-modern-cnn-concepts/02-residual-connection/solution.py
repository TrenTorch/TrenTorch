import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_multi_filter = load_solution("07-vision/01-convolutions/05-multiple-output-filters").conv2d_multi_filter
relu_forward = load_solution("02-deep-learning-core/02-activations/01-relu").relu_forward


def residual_block(x: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    padded = np.pad(x, ((0, 0), (1, 1), (1, 1)))
    conv_out = conv2d_multi_filter(padded, kernel)
    return relu_forward(x + conv_out)
