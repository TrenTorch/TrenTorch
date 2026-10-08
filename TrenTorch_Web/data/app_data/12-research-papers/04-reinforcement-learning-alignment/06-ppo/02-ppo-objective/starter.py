import numpy as np


def ppo_objective(ratios, advantages, eps):
    """
    ratios: probability ratios, shape (N,)
    advantages: advantage estimates, shape (N,)
    eps: clipping range

    Returns:
        The mean over the batch of min(r A, clip(r, 1 - eps, 1 + eps) A), as a float.
    """
    # TODO: Compute the clipped term for every sample and average the element-wise minimum (see Theory).
    pass
