
import numpy as np

from _load import load_solution

mse_gradient = load_solution("linear-regression-mse-gradient").mse_gradient


def ridge_grad(
    input: np.ndarray,
    weight: np.ndarray,
    bias: np.ndarray | None,
    target: np.ndarray,
    lam: float,
) -> tuple[np.ndarray, np.ndarray | None]:
    grad_weight, grad_bias = mse_gradient(input, weight, bias, target)
    return grad_weight + 2 * lam * weight, grad_bias
