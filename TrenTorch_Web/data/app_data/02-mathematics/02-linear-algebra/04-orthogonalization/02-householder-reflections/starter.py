import numpy as np


def householder_vector(x):
    """
    x: 1D array of floats

    Returns:
        A 1D array v of the same length such that the reflection across
        the plane perpendicular to v sends x to
        [-sign(x[0]) * norm(x), 0, ..., 0], with sign(0) = 1. Returns the
        zero vector when x is the zero vector. x must not be modified.
    """
    # TODO: Implement the direction from Theory, with the sign chosen to
    # avoid cancellation in the first entry.
    pass


def householder_matrix(v):
    """
    v: 1D array of floats, the mirror direction

    Returns:
        The n x n matrix I - 2 v v^T / (v^T v). Returns the identity when
        v is the zero vector.
    """
    # TODO: Implement the formula from Theory.
    pass


def apply_householder(v, a):
    """
    v: 1D array of floats, the mirror direction
    a: 1D vector or 2D matrix with len(v) rows

    Returns:
        The reflection of a (each column, for a matrix) with the same
        shape as a, computed without building the n x n matrix. Returns a
        copy of a when v is the zero vector. v and a must not be modified.
    """
    # TODO: Implement a - 2 v (v^T a) / (v^T v) from Theory.
    pass
