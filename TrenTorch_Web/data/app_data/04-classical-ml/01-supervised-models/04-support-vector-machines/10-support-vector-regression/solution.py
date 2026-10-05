import numpy as np

from _load import load_solution

epsilon_insensitive_loss = load_solution("support-vector-machines-epsilon-insensitive-loss").epsilon_insensitive_loss


def svr_objective(
    weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray, epsilon: float, lambda_reg: float
) -> float:
    predictions = X @ weight + bias
    return epsilon_insensitive_loss(predictions, y, epsilon=epsilon, reduction="mean") + lambda_reg * np.dot(
        weight, weight
    )


def svr_gradient(
    weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray, epsilon: float, lambda_reg: float
) -> tuple[np.ndarray, float]:
    residual = X @ weight + bias - y
    direction = np.where(np.abs(residual) > epsilon, np.sign(residual), 0.0)
    n = len(y)
    grad_weight = X.T @ direction / n + 2.0 * lambda_reg * weight
    grad_bias = float(np.sum(direction) / n)
    return grad_weight, grad_bias


def train_linear_svr(
    X: np.ndarray, y: np.ndarray, lr: float = 0.01, epochs: int = 1000, epsilon: float = 0.1, lambda_reg: float = 0.0
) -> tuple[np.ndarray, float]:
    weight = np.zeros(X.shape[1])
    bias = 0.0
    for _ in range(epochs):
        grad_weight, grad_bias = svr_gradient(weight, bias, X, y, epsilon, lambda_reg)
        weight = weight - lr * grad_weight
        bias = bias - lr * grad_bias
    return weight, bias
