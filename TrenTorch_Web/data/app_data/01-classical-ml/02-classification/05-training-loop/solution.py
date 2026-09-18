import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear
gd_step = load_solution("01-classical-ml/01-linear-regression/04-gd-step").gd_step
sigmoid = load_solution("01-classical-ml/02-classification/01-sigmoid").sigmoid
bce_gradient = load_solution("01-classical-ml/02-classification/03-bce-gradient").bce_gradient


def train_logistic_regression(
    input: np.ndarray,
    target: np.ndarray,
    lr: float,
    epochs: int,
) -> tuple[np.ndarray, np.ndarray]:
    weight = np.zeros((1, input.shape[1]))
    bias = np.zeros(1)
    target_2d = target.reshape(-1, 1)
    for _ in range(epochs):
        p = sigmoid(linear(input, weight, bias))
        grad_weight, grad_bias = bce_gradient(input, p, target_2d)
        weight, bias = gd_step(weight, bias, grad_weight, grad_bias, lr)
    return weight, bias
