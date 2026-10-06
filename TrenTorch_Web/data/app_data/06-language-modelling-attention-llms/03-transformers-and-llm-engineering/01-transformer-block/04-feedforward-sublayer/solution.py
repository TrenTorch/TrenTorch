
import numpy as np

from _load import load_solution

linear_forward = load_solution("dl-training-linear-forward").linear_forward
gelu_forward = load_solution("dl-activation-gelu").gelu_forward


def feedforward_sublayer(
    x: np.ndarray,
    weight1: np.ndarray,
    bias1: np.ndarray,
    weight2: np.ndarray,
    bias2: np.ndarray,
) -> np.ndarray:
    hidden = gelu_forward(linear_forward(x, weight1, bias1))
    return linear_forward(hidden, weight2, bias2)
