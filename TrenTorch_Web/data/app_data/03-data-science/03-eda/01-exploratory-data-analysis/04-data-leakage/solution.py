import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution

correlation = load_solution("02-mathematics/04-statistics/01-probability/10-covariance-correlation").correlation


def feature_target_correlations(x: np.ndarray, target: np.ndarray) -> np.ndarray:
    num_features = x.shape[1]
    return np.array([correlation(x[:, i], target) for i in range(num_features)])


def find_suspicious_features(x: np.ndarray, target: np.ndarray, threshold: float = 0.95) -> np.ndarray:
    correlations = feature_target_correlations(x, target)
    return np.where(np.abs(correlations) > threshold)[0]
