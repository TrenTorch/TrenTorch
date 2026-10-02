import numpy as np


def leading_principal_minors(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    return np.array([np.linalg.det(a[:k, :k]) for k in range(1, a.shape[0] + 1)])


def is_positive_definite_sylvester(a: np.ndarray) -> bool:
    a = np.asarray(a, dtype=float)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or not np.allclose(a, a.T):
        return False
    return bool(np.all(leading_principal_minors(a) > 0))


def classify_definiteness(a: np.ndarray, tol: float = 1e-10) -> str:
    a = np.asarray(a, dtype=float)
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("a must be square")
    if not np.allclose(a, a.T):
        raise ValueError("a must be symmetric")
    eigenvalues = np.linalg.eigvalsh(a)
    positive = int(np.sum(eigenvalues > tol))
    negative = int(np.sum(eigenvalues < -tol))
    zero = len(eigenvalues) - positive - negative
    if positive and negative:
        return "indefinite"
    if positive:
        return "positive semidefinite" if zero else "positive definite"
    if negative:
        return "negative semidefinite" if zero else "negative definite"
    return "zero"


def critical_point_type(hessian: np.ndarray, tol: float = 1e-10) -> str:
    verdicts = {
        "positive definite": "local minimum",
        "negative definite": "local maximum",
        "indefinite": "saddle point",
    }
    return verdicts.get(classify_definiteness(hessian, tol), "inconclusive")
