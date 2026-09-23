import numpy as np


def closed_form_linear_regression(input: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    n = input.shape[0]
    input_augmented = np.hstack([input, np.ones((n, 1))])
    target_col = target.reshape(-1, 1)

    theta = np.linalg.pinv(input_augmented) @ target_col

    weight = theta[:-1].T
    bias = theta[-1]
    return weight, bias
