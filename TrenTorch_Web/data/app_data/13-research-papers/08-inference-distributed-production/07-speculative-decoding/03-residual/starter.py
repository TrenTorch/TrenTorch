import numpy as np


def residual_distribution(p, q):
    """
    p: target model distribution over tokens
    q: draft model distribution over tokens, same shape

    Returns:
        The residual distribution max(p - q, 0), renormalized to sum to 1, used to resample after a rejection.
    """
    # TODO: Keep only the positive part of p - q and renormalize (see Theory).
    pass
