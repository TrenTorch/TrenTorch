import numpy as np


def rmsnorm(x, g, eps=1e-6):
    """
    x: activations, shape (..., d)
    g: learned per-feature gain, shape (d,)
    eps: small constant for stability

    Returns:
        x divided by its root-mean-square over the last axis, times g.
    """
    # TODO: Divide by the root mean square of each row and multiply by g (see Theory).
    pass
