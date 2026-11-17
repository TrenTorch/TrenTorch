import numpy as np


def batchnorm_train(x, gamma, beta, eps=1e-5):
    """
    x: a batch of activations, shape (N, D)
    gamma, beta: learned scale and shift, shape (D,)
    eps: small constant for numerical stability

    Returns:
        (out, mean, var): the normalized, scaled and shifted output, plus the
        per-feature batch mean and biased batch variance.
    """
    # TODO: Compute the batch statistics, normalize, then scale and shift (see Theory).
    pass
