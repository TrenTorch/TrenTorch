import numpy as np


def pairwise_row_dots(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b.T


def matrix_vector_product(matrix: np.ndarray, vector: np.ndarray) -> np.ndarray:
    return matrix @ vector
