import numpy as np


def qr_decompose(A):
    """
    A: an (m, n) NumPy array with linearly independent columns

    Returns:
        (Q, R): Q is (m, n) with orthonormal columns, R is (n, n)
        upper-triangular, such that Q @ R reconstructs A exactly.
    """
    # TODO: Implement Gram-Schmidt column by column, recording each
    # projection coefficient into R and each leftover norm into R's
    # diagonal, from Theory.
    pass
