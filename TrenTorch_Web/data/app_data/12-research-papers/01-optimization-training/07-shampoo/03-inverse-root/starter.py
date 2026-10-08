import numpy as np


def inverse_root(eigs, power):
    """
    eigs: positive eigenvalues of a preconditioner
    power: the root order, e.g. 4 for the fourth root

    Returns:
        The element-wise inverse root eigs ** (-1 / power).
    """
    # TODO: Raise each eigenvalue to minus one over the root order (see Theory).
    pass
