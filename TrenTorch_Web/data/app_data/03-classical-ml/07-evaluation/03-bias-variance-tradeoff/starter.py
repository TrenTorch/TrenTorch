import numpy as np


def polynomial_features(x: np.ndarray, degree: int) -> np.ndarray:
    """Returns shape (n_samples, degree+1): columns 1, x, x^2, ..., x^degree."""
    # TODO: np.stack a list of x**d for d in range(degree+1), axis=1.
    pass


def fit_polynomial(x: np.ndarray, y: np.ndarray, degree: int) -> np.ndarray:
    """Least-squares polynomial fit. Returns coefficients, shape (degree+1,)."""
    # TODO: polynomial_features(x, degree), then np.linalg.lstsq against y.
    pass


def predict_polynomial(coefficients: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Evaluates a fitted polynomial (from fit_polynomial) at new x values."""
    # TODO: polynomial_features(x, degree inferred from len(coefficients)-1),
    # then the design matrix times coefficients.
    pass


def bias_variance_decomposition(
    predictions: np.ndarray, targets: np.ndarray
) -> tuple[float, float, float]:
    """
    predictions: shape (n_models, n_test_points), each row is one
    independently-trained model's predictions on the same test points
    (e.g. one model per bootstrap-resampled training set).
    targets: shape (n_test_points,), the TRUE (noiseless) function
    values at those test points.

    Returns:
        (bias_squared, variance, bias_squared + variance): the squared-
        error bias-variance decomposition, averaged over test points.
    """
    # TODO: mean_prediction = predictions.mean(axis=0), the average
    # model's prediction at each test point.
    # bias_squared = mean((mean_prediction - targets)^2)
    # variance = mean(predictions.var(axis=0)) -- how much predictions
    # at each test point vary ACROSS models, averaged over test points.
    pass
