import numpy as np


def lu_decompose(A):
    """
    A: a square (n, n) NumPy array that does not require row swaps
       (every pivot encountered during elimination is non-zero)

    Returns:
        (L, U): L is lower-triangular with 1s on the diagonal, U is
        upper-triangular, such that L @ U reconstructs A exactly.
    """
    # TODO: Implement Gaussian elimination on a copy of A (building U),
    # recording each elimination multiplier into L, from Theory.
    pass
