import numpy as np


def normalize_rows(data: np.ndarray) -> np.ndarray:
    row_means = data.mean(axis=1, keepdims=True)
    row_stds = data.std(axis=1, keepdims=True)
    return (data - row_means) / row_stds


def pairwise_differences(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a[np.newaxis, :] - b[:, np.newaxis]


def scale_columns(matrix: np.ndarray, scale_factors: np.ndarray) -> np.ndarray:
    return matrix * scale_factors
