import numpy as np


def is_symmetric(a: np.ndarray) -> bool:
    return np.allclose(a, a.T)


def quadratic_form(a: np.ndarray, x: np.ndarray) -> float:
    return float(x @ a @ x)


def is_positive_definite(a: np.ndarray) -> bool:
    if not is_symmetric(a):
        return False
    eigenvalues = np.linalg.eigvalsh(a)
    return bool(np.all(eigenvalues > 0))
