import numpy as np


def ridge_solution(X, y, lam):
    """
    X: design matrix, shape (n, p)
    y: targets, shape (n,)
    lam: ridge penalty (non-negative)

    Returns:
        w = (X^T X + lam I)^(-1) X^T y, shape (p,).
    """
    # TODO: Solve the regularized normal equations (see Theory).
    pass
