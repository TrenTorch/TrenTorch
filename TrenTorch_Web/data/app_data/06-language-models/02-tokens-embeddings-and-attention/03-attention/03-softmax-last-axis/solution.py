
import numpy as np

from _load import load_solution

softmax_axis1 = load_solution("classification-softmax-cce").softmax


def softmax_last_axis(Z: np.ndarray) -> np.ndarray:
    original_shape = Z.shape
    Z_2d = Z.reshape(-1, original_shape[-1])
    result_2d = softmax_axis1(Z_2d)
    return result_2d.reshape(original_shape)
