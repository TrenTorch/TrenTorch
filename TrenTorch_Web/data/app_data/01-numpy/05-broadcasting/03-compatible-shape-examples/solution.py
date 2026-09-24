import numpy as np


def add_scalar(matrix: np.ndarray, scalar: float) -> np.ndarray:
    return matrix + scalar


def add_row_vector(matrix: np.ndarray, row_vector: np.ndarray) -> np.ndarray:
    return matrix + row_vector


def add_column_vector(matrix: np.ndarray, col_values: np.ndarray) -> np.ndarray:
    return matrix + col_values[:, np.newaxis]


def outer_sum(row_values: np.ndarray, col_values: np.ndarray) -> np.ndarray:
    return row_values[np.newaxis, :] + col_values[:, np.newaxis]
