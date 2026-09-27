import numpy as np


def rank(A):
    """
    A: an (m, n) NumPy array

    Returns:
        The rank of A: the number of linearly independent rows,
        computed via row-reduction (skip a column with no usable pivot
        rather than treating it as an error).
    """
    # TODO: Implement row-reduction with a separate pivot-row/pivot-
    # column pointer, counting pivots found, from Theory.
    pass


def nullity(A):
    """
    A: an (m, n) NumPy array

    Returns:
        The nullity of A: A.shape[1] - rank(A), per the Rank-Nullity
        Theorem.
    """
    # TODO: Implement using rank(A) from Theory's formula.
    pass
