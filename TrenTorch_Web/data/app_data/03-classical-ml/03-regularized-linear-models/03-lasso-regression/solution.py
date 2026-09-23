import numpy as np


def soft_threshold(x: np.ndarray, threshold: float) -> np.ndarray:
    return np.sign(x) * np.maximum(np.abs(x) - threshold, 0.0)


def lasso_regression_coordinate_descent(
    input: np.ndarray, target: np.ndarray, alpha: float = 1.0, epochs: int = 200
) -> tuple[np.ndarray, np.ndarray]:
    n, d = input.shape
    x_mean = input.mean(axis=0)
    y_mean = target.mean()
    x_centered = input - x_mean
    y_centered = target - y_mean

    weight = np.zeros(d)
    for _ in range(epochs):
        for j in range(d):
            residual = y_centered - x_centered @ weight + x_centered[:, j] * weight[j]
            rho_j = (x_centered[:, j] @ residual) / n
            z_j = (x_centered[:, j] @ x_centered[:, j]) / n
            weight[j] = soft_threshold(rho_j, alpha) / z_j if z_j > 0 else 0.0

    bias = y_mean - x_mean @ weight
    return weight.reshape(1, -1), np.array([bias])
