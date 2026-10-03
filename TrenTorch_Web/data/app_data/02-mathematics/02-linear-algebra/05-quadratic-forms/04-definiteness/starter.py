import numpy as np


def leading_principal_minors(a: np.ndarray) -> np.ndarray:
    """
    a: n x n array

    Returns:
        A 1D array of length n whose entry k - 1 is the determinant of
        the top-left k x k block of a.
    """
    # TODO: Take the determinant of each growing top-left block.
    pass


def is_positive_definite_sylvester(a: np.ndarray) -> bool:
    """
    a: a 2D array

    Returns:
        True if a is square, symmetric (np.allclose) and every leading
        principal minor is strictly positive, otherwise False. Do not
        compute eigenvalues.
    """
    # TODO: Apply Sylvester's criterion from Theory.
    pass


def classify_definiteness(a: np.ndarray, tol: float = 1e-10) -> str:
    """
    a: a square, symmetric 2D array
    tol: eigenvalues within tol of zero count as zero

    Returns:
        One of "positive definite", "positive semidefinite",
        "negative definite", "negative semidefinite", "indefinite" or
        "zero" ("zero" only when every eigenvalue is within tol of zero).

    Raises:
        ValueError: if a is not square or not symmetric (np.allclose).
    """
    # TODO: Classify by the signs of the eigenvalues, as in Theory.
    pass


def critical_point_type(hessian: np.ndarray, tol: float = 1e-10) -> str:
    """
    hessian: the Hessian at a point where the gradient is zero

    Returns:
        "local minimum" (positive definite), "local maximum" (negative
        definite), "saddle point" (indefinite) or "inconclusive"
        (semidefinite or zero).

    Raises:
        ValueError: if the Hessian is not square and symmetric.
    """
    # TODO: Map the class from classify_definiteness to a verdict.
    pass
