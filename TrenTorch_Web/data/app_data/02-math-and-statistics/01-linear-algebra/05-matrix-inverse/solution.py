import numpy as np


def determinant(a: np.ndarray) -> float:
    return float(np.linalg.det(a))


def is_invertible(a: np.ndarray) -> bool:
    return not np.isclose(determinant(a), 0.0)


def matrix_inverse(a: np.ndarray) -> np.ndarray:
    if not is_invertible(a):
        raise np.linalg.LinAlgError("matrix is singular, no inverse exists")
    return np.linalg.inv(a)
