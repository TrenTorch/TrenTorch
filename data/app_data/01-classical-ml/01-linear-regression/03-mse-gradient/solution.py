import numpy as np


def mse_gradient(
    input: np.ndarray,
    weight: np.ndarray,
    bias: np.ndarray | None,
    target: np.ndarray,
) -> tuple[np.ndarray, np.ndarray | None]:
    prediction = input @ weight.T
    if bias is not None:
        prediction = prediction + bias
    element_count = prediction.size
    grad_prediction = (2.0 / element_count) * (prediction - target)
    grad_weight = grad_prediction.T @ input
    grad_bias = None if bias is None else grad_prediction.sum(axis=0)
    return grad_weight, grad_bias
