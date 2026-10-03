import numpy as np


def rbf_kernel(
    input_a: np.ndarray, input_b: np.ndarray, length_scale: float, variance: float
) -> np.ndarray:
    """
    input_a: shape (n_a, n_features)
    input_b: shape (n_b, n_features)

    Returns:
        shape (n_a, n_b): the RBF ("squared exponential") kernel,
        variance * exp(-0.5 * ||x_a - x_b||^2 / length_scale^2), between
        every pair of rows.
    """
    # TODO: Same broadcasting pattern as 01-knn's pairwise_distances,
    # squared distance instead of a square root, then plug into the
    # RBF formula.
    pass


def gp_predict(
    input_train: np.ndarray,
    targets_train: np.ndarray,
    input_test: np.ndarray,
    length_scale: float,
    variance: float,
    noise: float,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns:
        mean: shape (n_test,), the posterior mean prediction at every
        test point.
        variance_out: shape (n_test,), the posterior variance
        (uncertainty) at every test point.
    """
    # TODO: Build three kernel matrices with rbf_kernel:
    #   k_train_train (n_train, n_train), plus noise * I on the diagonal
    #   k_train_test  (n_train, n_test)
    #   k_test_test   (n_test, n_test)
    # Standard GP posterior formulas:
    #   mean       = k_train_test.T @ inv(k_train_train) @ targets_train
    #   covariance = k_test_test - k_train_test.T @ inv(k_train_train) @ k_train_test
    # Return mean and the diagonal of covariance (clipped at 0, floating
    # point can make it very slightly negative).
    pass
