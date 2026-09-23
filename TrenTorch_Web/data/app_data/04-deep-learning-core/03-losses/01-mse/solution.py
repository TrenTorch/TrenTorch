import numpy as np


def mse_loss_forward(input: np.ndarray, target: np.ndarray, reduction: str = "mean"):
    squared_error = (input - target) ** 2
    if reduction == "none":
        return squared_error
    if reduction == "sum":
        return squared_error.sum()
    return squared_error.mean()


def mse_loss_backward(
    input: np.ndarray, target: np.ndarray, reduction: str = "mean", grad_output=1.0
) -> np.ndarray:
    grad = 2.0 * (input - target)
    if reduction == "mean":
        grad = grad / input.size
    return grad_output * grad
