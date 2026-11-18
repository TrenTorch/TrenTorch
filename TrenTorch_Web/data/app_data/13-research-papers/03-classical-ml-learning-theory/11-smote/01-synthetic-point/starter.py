import numpy as np


def smote_point(x, neighbor, u):
    """
    x: a minority-class sample, shape (d,)
    neighbor: one of its nearest minority-class neighbors, shape (d,)
    u: a uniform random number in [0, 1]

    Returns:
        The synthetic point x + u * (neighbor - x), on the segment between them.
    """
    # TODO: Move from x toward its neighbor by the fraction u (see Theory).
    pass
