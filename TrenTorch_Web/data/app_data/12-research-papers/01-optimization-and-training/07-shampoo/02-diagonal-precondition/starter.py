import numpy as np


def precondition_diag(L, G, R):
    """
    L: diagonal of the left preconditioner, shape (m,), positive
    G: gradient matrix, shape (m, n)
    R: diagonal of the right preconditioner, shape (n,), positive

    Returns:
        The preconditioned gradient L^{-1/4} G R^{-1/4}, assuming diagonal preconditioners.
    """
    # TODO: Scale each row by L^{-1/4} and each column by R^{-1/4} (see Theory).
    pass
