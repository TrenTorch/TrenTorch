import numpy as np


def functional_margin(weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray) -> np.ndarray:
    scores = X @ weight + bias
    return y * scores


def geometric_margin(weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray) -> np.ndarray:
    return functional_margin(weight, bias, X, y) / np.linalg.norm(weight)


def dataset_margin(weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray) -> float:
    return float(np.min(geometric_margin(weight, bias, X, y)))
