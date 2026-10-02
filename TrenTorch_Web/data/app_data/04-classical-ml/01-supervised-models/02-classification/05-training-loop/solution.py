
import numpy as np

from _load import load_solution

linear = load_solution("linear-regression-hypothesis-function").linear
gd_step = load_solution("linear-regression-gd-step").gd_step
sigmoid = load_solution("classification-sigmoid").sigmoid
bce_gradient = load_solution("classification-bce-gradient").bce_gradient


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
