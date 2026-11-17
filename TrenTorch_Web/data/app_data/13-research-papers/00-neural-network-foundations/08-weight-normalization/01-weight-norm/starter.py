import numpy as np


def weight_norm(v, g):
    """
    v: unconstrained direction parameters, shape (out, in)
    g: per-output scale parameters, shape (out,)

    Returns:
        W with each row equal to g[i] * v[i] / ||v[i]||.
    """
    # TODO: Normalize each row of v to unit length and multiply by g (see Theory).
    pass
