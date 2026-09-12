import numpy as np


def ridge_regression_closed_form(
    input: np.ndarray, target: np.ndarray, alpha: float = 1.0
) -> tuple[np.ndarray, np.ndarray]:
    n, d = input.shape
    input_augmented = np.hstack([input, np.ones((n, 1))])
    target_col = target.reshape(-1, 1)

    penalty = alpha * np.eye(d + 1)
    penalty[-1, -1] = 0.0  # never regularize the bias term

    theta = np.linalg.inv(input_augmented.T @ input_augmented + penalty) @ input_augmented.T @ target_col

    weight = theta[:-1].T
    bias = theta[-1]
    return weight, bias
