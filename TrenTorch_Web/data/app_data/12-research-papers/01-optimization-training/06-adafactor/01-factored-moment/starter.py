import numpy as np


def factored_second_moment(row, col):
    """
    row: row sums of the second-moment matrix, shape (n,)
    col: column sums of the second-moment matrix, shape (m,)

    Returns:
        The rank-one approximation V ~ outer(row, col) / sum(row), shape (n, m).
    """
    # TODO: Form the outer product and normalize by the total mass (see Theory).
    pass
