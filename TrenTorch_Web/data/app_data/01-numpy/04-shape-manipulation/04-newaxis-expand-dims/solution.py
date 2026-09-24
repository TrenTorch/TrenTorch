import numpy as np


def to_column_vector(arr: np.ndarray) -> np.ndarray:
    return arr[:, np.newaxis]


def to_row_vector(arr: np.ndarray) -> np.ndarray:
    return arr[np.newaxis, :]


def add_dimension_at(arr: np.ndarray, axis: int) -> np.ndarray:
    return np.expand_dims(arr, axis=axis)
