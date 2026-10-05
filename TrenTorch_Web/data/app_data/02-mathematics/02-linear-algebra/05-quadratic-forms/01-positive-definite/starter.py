import numpy as np


def is_symmetric(a: np.ndarray) -> bool:
    """
    True iff a == a.T (elementwise, within floating-point tolerance).
    """
    pass


def quadratic_form(a: np.ndarray, x: np.ndarray) -> float:
    """
    Computes x^T @ A @ x, a single scalar. This is the expression whose
    sign positive-definiteness is defined by.
    """
    pass


def is_positive_definite(a: np.ndarray) -> bool:
    """
    `a` (assumed square) is positive-definite iff it is symmetric AND
    every eigenvalue is strictly positive. Use np.linalg.eigvalsh
    (the eigenvalues-only sibling of 06-eigenvalues-eigenvectors'
    np.linalg.eigh, for real symmetric matrices) rather than computing
    quadratic_form for every possible x, which is the actual
    definition but impossible to check exhaustively.
    """
    pass
