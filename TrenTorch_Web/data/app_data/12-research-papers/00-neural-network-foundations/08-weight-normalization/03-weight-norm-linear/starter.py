import numpy as np


def weight_norm_linear(x, v, g, b):
    """
    x: inputs, shape (N, in)
    v: direction parameters, shape (out, in)
    g: per-output scales, shape (out,)
    b: bias, shape (out,)

    Returns:
        x @ W.T + b, where W is the weight-normalized matrix from v and g.
    """
    # TODO: Build W from v and g, then apply the affine map (see Theory).
    pass
