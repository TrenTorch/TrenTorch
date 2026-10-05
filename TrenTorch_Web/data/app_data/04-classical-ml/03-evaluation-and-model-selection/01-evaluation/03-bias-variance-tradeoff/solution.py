import numpy as np


def polynomial_features(x: np.ndarray, degree: int) -> np.ndarray:
    return np.stack([x**d for d in range(degree + 1)], axis=1)


def fit_polynomial(x: np.ndarray, y: np.ndarray, degree: int) -> np.ndarray:
    design_matrix = polynomial_features(x, degree)
    coefficients, _, _, _ = np.linalg.lstsq(design_matrix, y, rcond=None)
    return coefficients


def predict_polynomial(coefficients: np.ndarray, x: np.ndarray) -> np.ndarray:
    degree = coefficients.shape[0] - 1
    design_matrix = polynomial_features(x, degree)
    return design_matrix @ coefficients


def bias_variance_decomposition(
    predictions: np.ndarray, targets: np.ndarray
) -> tuple[float, float, float]:
    mean_prediction = predictions.mean(axis=0)
    bias_squared = float(np.mean((mean_prediction - targets) ** 2))
    variance = float(np.mean(predictions.var(axis=0)))
    return bias_squared, variance, bias_squared + variance
