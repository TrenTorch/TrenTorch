import numpy as np


def _is_square_symmetric(a: np.ndarray) -> bool:
    return a.ndim == 2 and a.shape[0] == a.shape[1] and bool(np.allclose(a, a.T))


def is_negative_definite(a: np.ndarray) -> bool:
    a = np.asarray(a, dtype=float)
    if not _is_square_symmetric(a):
        return False
    return bool(np.linalg.eigvalsh(a)[-1] < 0)


def is_negative_semidefinite(a: np.ndarray, tol: float = 1e-10) -> bool:
    a = np.asarray(a, dtype=float)
    if not _is_square_symmetric(a):
        return False
    return bool(np.linalg.eigvalsh(a)[-1] <= tol)


def quadratic_maximizer(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if not is_negative_definite(a):
        raise ValueError("a must be negative definite for a unique maximizer to exist")
    return np.linalg.solve(a, -b)
