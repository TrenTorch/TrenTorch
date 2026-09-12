import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

mse_gradient = load_solution("01-classical-ml/01-linear-regression/03-mse-gradient").mse_gradient
gd_step = load_solution("01-classical-ml/01-linear-regression/04-gd-step").gd_step


def train_linear_regression(
    input: np.ndarray,
    target: np.ndarray,
    lr: float,
    epochs: int,
) -> tuple[np.ndarray, np.ndarray]:
    weight = np.zeros((1, input.shape[1]))
    bias = np.zeros(1)
    target_2d = target.reshape(-1, 1)
    for _ in range(epochs):
        grad_weight, grad_bias = mse_gradient(input, weight, bias, target_2d)
        weight, bias = gd_step(weight, bias, grad_weight, grad_bias, lr)
    return weight, bias
