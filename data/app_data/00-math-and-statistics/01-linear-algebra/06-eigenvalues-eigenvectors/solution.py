import numpy as np


def eigen_decomposition(a: np.ndarray):
    eigenvalues, eigenvectors = np.linalg.eigh(a)
    return eigenvalues, eigenvectors


def verify_eigenpair(a: np.ndarray, eigenvalue: float, eigenvector: np.ndarray) -> bool:
    return np.allclose(a @ eigenvector, eigenvalue * eigenvector, atol=1e-8)
