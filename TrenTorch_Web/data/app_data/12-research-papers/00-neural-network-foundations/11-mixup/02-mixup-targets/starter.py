import numpy as np


def mixup_targets(y, perm, lam):
    """
    y: one-hot label matrix, shape (N, C)
    perm: the same permutation used for the inputs
    lam: the same mixing weight used for the inputs

    Returns:
        The mixed soft targets, shape (N, C).
    """
    # TODO: Blend the one-hot labels with the same permutation and weight.
    pass
