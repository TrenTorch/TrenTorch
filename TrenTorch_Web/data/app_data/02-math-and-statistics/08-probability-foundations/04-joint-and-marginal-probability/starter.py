import numpy as np


def joint_from_independent(marginal_x, marginal_y):
    """
    marginal_x: 1D array-like, P(X = x_i) for each i, a valid PMF
    marginal_y: 1D array-like, P(Y = y_j) for each j, a valid PMF

    Returns:
        A 2D NumPy array `joint` of shape (len(marginal_x), len(marginal_y))
        where joint[i, j] = P(X=x_i, Y=y_j), computed AS IF X and Y were
        independent: P(X=x_i, Y=y_j) = P(X=x_i) * P(Y=y_j).
    """
    # TODO: Implement the independence formula as an outer product.
    pass


def marginalize(joint, axis):
    """
    joint: 2D array-like joint PMF, joint[i, j] = P(X=x_i, Y=y_j)
    axis: which axis to sum OUT (0 sums out X, leaving the Y marginal;
        1 sums out Y, leaving the X marginal) -- same convention as
        NumPy's own `axis` argument to `.sum()`.

    Returns:
        The 1D marginal distribution obtained by summing `joint` over
        the given axis.
    """
    # TODO: Implement marginalization by summing over `axis`.
    pass
