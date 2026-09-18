import numpy as np


def svd(a: np.ndarray):
    u, singular_values, vt = np.linalg.svd(a, full_matrices=False)
    return u, singular_values, vt


def reconstruct_from_svd(u: np.ndarray, singular_values: np.ndarray, vt: np.ndarray) -> np.ndarray:
    return u @ np.diag(singular_values) @ vt


def low_rank_approximation(a: np.ndarray, k: int) -> np.ndarray:
    u, singular_values, vt = svd(a)
    return u[:, :k] @ np.diag(singular_values[:k]) @ vt[:k, :]
