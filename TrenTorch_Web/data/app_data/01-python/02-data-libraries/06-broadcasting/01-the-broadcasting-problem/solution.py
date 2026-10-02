import numpy as np


def add_row_with_loop(matrix: np.ndarray, row: np.ndarray) -> np.ndarray:
    result = np.empty_like(matrix)
    for i in range(matrix.shape[0]):
        result[i] = matrix[i] + row
    return result


def add_row_with_broadcasting(matrix: np.ndarray, row: np.ndarray) -> np.ndarray:
    return matrix + row
