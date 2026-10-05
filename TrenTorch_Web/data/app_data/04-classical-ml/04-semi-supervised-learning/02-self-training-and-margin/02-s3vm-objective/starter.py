import numpy as np


def s3vm_objective(
    w: np.ndarray,
    b: float,
    X_l: np.ndarray,
    y_l: np.ndarray,
    X_u: np.ndarray,
    C: float,
    C_u: float,
) -> float:
    """
    0.5 ||w||^2 + C * sum_l max(0, 1 - y f) + C_u * sum_u max(0, 1 - |f|),
    with f = X w + b. Raise ValueError for labels outside {-1, +1}, negative
    C or C_u, or shape mismatches.
    """
    pass
