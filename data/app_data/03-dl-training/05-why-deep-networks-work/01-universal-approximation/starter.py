import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def random_hidden_features(x: np.ndarray, num_hidden: int, rng: np.random.RandomState) -> np.ndarray:
    """
    Builds a "one wide hidden layer" of sigmoid neurons applied to 1D
    input `x`: each of `num_hidden` neurons gets its OWN random weight
    and bias, producing a (len(x), num_hidden) matrix of activations,
    one column per neuron.
    """
    weight = rng.randn(num_hidden) * 5.0
    bias = rng.randn(num_hidden) * 5.0
    pass


def fit_output_weights(hidden: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Given the hidden layer's activations and a target `y`, solves for the
    OUTPUT layer's weights via least squares: the linear combination of
    hidden units that best matches `y`.
    """
    pass


def approximate_function(
    x: np.ndarray, y: np.ndarray, num_hidden: int, rng: np.random.RandomState
) -> tuple[np.ndarray, float]:
    """
    Fits a one-hidden-layer network to approximate the function that maps
    `x` to `y`, using `random_hidden_features` and `fit_output_weights`
    (both above). Returns (predictions, mean squared error).
    """
    pass
