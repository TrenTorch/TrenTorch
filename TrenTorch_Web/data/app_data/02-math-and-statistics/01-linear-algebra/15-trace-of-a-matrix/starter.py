import numpy as np


def trace(A):
    """
    A: a square (n, n) NumPy array

    Returns:
        The sum of A's diagonal entries.
    """
    # TODO: Implement tr(A) = Sum_i A[i, i] from Theory.
    pass


def trace_of_product(A, B):
    """
    A: shape (m, n)
    B: shape (n, m), so A @ B is a valid square (m, m) matrix

    Returns:
        trace(A @ B), computed WITHOUT forming the full product A @ B --
        use the cyclic-property shortcut from Theory instead.
    """
    # TODO: Implement using the sum(A * B.T) identity from Theory.
    pass
