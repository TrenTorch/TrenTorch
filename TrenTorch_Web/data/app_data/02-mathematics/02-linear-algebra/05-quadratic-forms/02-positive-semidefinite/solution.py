import numpy as np


def is_positive_semidefinite(a: np.ndarray, tol: float = 1e-10) -> bool:
    a = np.asarray(a, dtype=float)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or not np.allclose(a, a.T):
        return False
    return bool(np.linalg.eigvalsh(a)[0] >= -tol)


def gram_matrix(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return x @ x.T


def nearest_psd(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    symmetric = (a + a.T) / 2.0
    eigenvalues, eigenvectors = np.linalg.eigh(symmetric)
    clipped = np.clip(eigenvalues, 0.0, None)
    result = (eigenvectors * clipped) @ eigenvectors.T
    return (result + result.T) / 2.0
