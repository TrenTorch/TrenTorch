import numpy as np

from _load import load_solution

householder_vector = load_solution("math-householder-reflections").householder_vector
apply_householder = load_solution("math-householder-reflections").apply_householder


def householder_qr(a):
    """
    a: m x n float array with m >= n

    Returns:
        (Q, R): Q is m x m and orthogonal, R is m x n with exact zeros
        below the diagonal, and Q @ R equals a. Uses one Householder
        mirror per column; skips a column whose mirror direction is zero.
        a must not be modified.
    """
    # TODO: Clear each column below the diagonal with a mirror, as in Theory,
    # and accumulate the mirrors into Q.
    pass


def back_substitution(r, y):
    """
    r: n x n upper-triangular float array with a nonzero diagonal
    y: 1D float array of length n

    Returns:
        The 1D array x with r @ x == y, found from the last row upward
        with a loop (do not call np.linalg.solve).
    """
    # TODO: Solve from the last row upward, as in Theory.
    pass


def least_squares_qr(a, b):
    """
    a: m x n float array with full column rank, m >= n
    b: 1D float array of length m

    Returns:
        The 1D array x of length n minimising the squared error of
        a @ x - b, using householder_qr and back_substitution. Do not form
        a.T @ a.
    """
    # TODO: Reduce to the triangular system from Theory.
    pass
