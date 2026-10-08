import numpy as np


def ntm_write(memory, w, erase, add):
    """
    memory: memory matrix, shape (N, M)
    w: write weights over rows, shape (N,)
    erase: erase vector, shape (M,), values in [0, 1]
    add: add vector, shape (M,)

    Returns:
        The updated memory: each row is erased by w times erase, then gets w times add.
    """
    # TODO: Erase then add, with each row scaled by its write weight (see Theory).
    pass
