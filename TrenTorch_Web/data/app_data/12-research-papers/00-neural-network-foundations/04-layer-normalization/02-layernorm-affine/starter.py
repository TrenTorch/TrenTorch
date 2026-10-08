import numpy as np


def layernorm(x, gamma, beta, eps=1e-5):
    """
    x: activations, shape (..., D)
    gamma, beta: learned per-feature scale and shift, shape (D,)
    eps: small constant for numerical stability

    Returns:
        The layer-normalized output, scaled and shifted per feature.
    """
    # TODO: Normalize over the last axis, then apply gamma and beta (see Theory).
    pass
