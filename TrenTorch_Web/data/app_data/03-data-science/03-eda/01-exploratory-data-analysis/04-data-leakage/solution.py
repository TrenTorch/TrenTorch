
import numpy as np

from _load import load_solution

correlation = load_solution("math-expectation-variance-covariance").correlation


def feature_target_correlations(x: np.ndarray, target: np.ndarray) -> np.ndarray:
    num_features = x.shape[1]
    return np.array([correlation(x[:, i], target) for i in range(num_features)])


def find_suspicious_features(x: np.ndarray, target: np.ndarray, threshold: float = 0.95) -> np.ndarray:
    correlations = feature_target_correlations(x, target)
    return np.where(np.abs(correlations) > threshold)[0]
