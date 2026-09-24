import numpy as np


def determinant(matrix: np.ndarray) -> float:
    return np.linalg.det(matrix)


def is_invertible(matrix: np.ndarray) -> bool:
    return bool(abs(determinant(matrix)) > 1e-10)


def safe_inverse(matrix: np.ndarray):
    if not is_invertible(matrix):
        return None
    return np.linalg.inv(matrix)


def verify_inverse(matrix: np.ndarray, inverse: np.ndarray) -> bool:
    identity = np.eye(len(matrix))
    return bool(np.allclose(matrix @ inverse, identity))
