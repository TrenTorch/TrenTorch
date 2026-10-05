import numpy as np


def maskgit_loss(logits, targets, mask):
    """Compute MaskGIT loss.

    Args:
        logits: Model logits, shape (N, L, V).
        targets: Target token indices, shape (N, L).
        mask: Binary mask (1 for positions to predict), shape (N, L).

    Returns:
        Scalar loss.
    """
    pass
