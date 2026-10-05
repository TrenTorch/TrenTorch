import numpy as np


def mixup_inputs(x, perm, lam):
    """
    x: a batch of inputs, shape (N, ...)
    perm: a permutation of range(N) pairing each example with another
    lam: mixing weight in [0, 1]

    Returns:
        lam * x + (1 - lam) * x[perm], the mixed batch.
    """
    # TODO: Blend each example with its permuted partner (see Theory).
    pass
