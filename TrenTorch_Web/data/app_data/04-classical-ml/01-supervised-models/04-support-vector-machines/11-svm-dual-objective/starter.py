import numpy as np


def dual_objective(alpha: np.ndarray, y: np.ndarray, K: np.ndarray) -> float:
    """
    W(alpha) = sum(alpha) - 0.5 * sum_ij alpha_i alpha_j y_i y_j K_ij.
    Raise ValueError if alpha and y do not have length n, or K is not n by n.
    """
    pass


def is_dual_feasible(alpha: np.ndarray, y: np.ndarray, C: float, tol: float = 1e-9) -> bool:
    """
    True when 0 <= alpha_i <= C (within tol) for every i and sum(alpha_i * y_i)
    is zero (within tol). Raise ValueError for C < 0 or mismatched shapes.
    """
    pass
