import numpy as np


def radius_feature(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.sqrt(x**2 + y**2)


def ratio_feature(numerator: np.ndarray, denominator: np.ndarray) -> np.ndarray:
    return numerator / denominator
