import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def build_features(x: np.ndarray, weight: np.ndarray, bias: np.ndarray) -> np.ndarray:
    return sigmoid(np.outer(x, weight) + bias)


def fit_min_norm(hidden: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.linalg.pinv(hidden) @ y


def train_and_test_mse(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    num_features: int,
    rng: np.random.RandomState,
) -> tuple[float, float]:
    weight = rng.randn(num_features)
    bias = rng.randn(num_features)

    hidden_train = build_features(x_train, weight, bias)
    hidden_test = build_features(x_test, weight, bias)

    output_weight = fit_min_norm(hidden_train, y_train)

    train_pred = hidden_train @ output_weight
    test_pred = hidden_test @ output_weight

    train_mse = float(np.mean((train_pred - y_train) ** 2))
    test_mse = float(np.mean((test_pred - y_test) ** 2))
    return train_mse, test_mse
