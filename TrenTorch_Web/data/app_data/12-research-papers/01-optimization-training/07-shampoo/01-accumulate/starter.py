import numpy as np


def accumulate_preconditioners(L, R, G):
    """
    L: left preconditioner, shape (m, m); R: right preconditioner, shape (n, n)
    G: gradient matrix, shape (m, n)

    Returns:
        The updated (L, R) after adding G G^T to L and G^T G to R.
    """
    # TODO: Add the two gram matrices of G to the running preconditioners (see Theory).
    pass
