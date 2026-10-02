import numpy as np


def rbf_kernel(
    input_a: np.ndarray, input_b: np.ndarray, length_scale: float, variance: float
) -> np.ndarray:
    diff = input_a[:, np.newaxis, :] - input_b[np.newaxis, :, :]
    squared_distances = np.sum(diff**2, axis=-1)
    return variance * np.exp(-0.5 * squared_distances / length_scale**2)


def gp_predict(
    input_train: np.ndarray,
    targets_train: np.ndarray,
    input_test: np.ndarray,
    length_scale: float,
    variance: float,
    noise: float,
) -> tuple[np.ndarray, np.ndarray]:
    n_train = input_train.shape[0]

    k_train_train = rbf_kernel(input_train, input_train, length_scale, variance) + noise * np.eye(
        n_train
    )
    k_train_test = rbf_kernel(input_train, input_test, length_scale, variance)
    k_test_test = rbf_kernel(input_test, input_test, length_scale, variance)

    k_train_train_inv = np.linalg.inv(k_train_train)

    mean = k_train_test.T @ k_train_train_inv @ targets_train
    covariance = k_test_test - k_train_test.T @ k_train_train_inv @ k_train_test
    variance_out = np.clip(np.diag(covariance), 0.0, None)

    return mean, variance_out
