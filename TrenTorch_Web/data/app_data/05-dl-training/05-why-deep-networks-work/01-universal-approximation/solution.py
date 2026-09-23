import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def random_hidden_features(x: np.ndarray, num_hidden: int, rng: np.random.RandomState) -> np.ndarray:
    weight = rng.randn(num_hidden) * 5.0
    bias = rng.randn(num_hidden) * 5.0
    return sigmoid(np.outer(x, weight) + bias)


def fit_output_weights(hidden: np.ndarray, y: np.ndarray) -> np.ndarray:
    weight, *_ = np.linalg.lstsq(hidden, y, rcond=None)
    return weight


def approximate_function(
    x: np.ndarray, y: np.ndarray, num_hidden: int, rng: np.random.RandomState
) -> tuple[np.ndarray, float]:
    hidden = random_hidden_features(x, num_hidden, rng)
    output_weight = fit_output_weights(hidden, y)
    pred = hidden @ output_weight
    mse = float(np.mean((pred - y) ** 2))
    return pred, mse
