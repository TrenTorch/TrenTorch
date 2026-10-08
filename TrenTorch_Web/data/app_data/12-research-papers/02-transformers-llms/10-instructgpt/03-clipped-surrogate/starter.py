import numpy as np


def clipped_surrogate(ratio, advantage, eps=0.2):
    """
    ratio: pi_new(a | s) / pi_old(a | s), per sample
    advantage: estimated advantage per sample
    eps: clipping range

    Returns:
        min(ratio * A, clip(ratio, 1 - eps, 1 + eps) * A), per sample.
    """
    # TODO: Compute both terms and take their element-wise minimum (see Theory).
    pass
