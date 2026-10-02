import numpy as np


def is_independent(joint, tol=1e-9):
    """
    joint: 2D array-like joint PMF, joint[i, j] = P(X=x_i, Y=y_j)
    tol: absolute tolerance for the equality check

    Returns:
        True if X and Y are independent under this joint distribution,
        i.e. joint == outer(marginal_x, marginal_y) within `tol`.
    """
    # TODO: Compute both marginals, then compare joint to their outer
    # product, from Theory.
    pass


def conditional_pmf_given_y(joint, y_index):
    """
    joint: 2D array-like joint PMF, joint[i, j] = P(X=x_i, Y=y_j)
    y_index: the index j of the Y value to condition on

    Returns:
        A 1D NumPy array: P(X=x_i | Y=y_index) for each i, from Theory.
    """
    # TODO: Implement P(X|Y=y) = P(X, Y=y) / P(Y=y) from Theory.
    pass
