import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

softmax_axis1 = load_solution("01-classical-ml/02-classification/06-softmax-cce").softmax


def softmax_last_axis(Z: np.ndarray) -> np.ndarray:
    original_shape = Z.shape
    Z_2d = Z.reshape(-1, original_shape[-1])
    result_2d = softmax_axis1(Z_2d)
    return result_2d.reshape(original_shape)
