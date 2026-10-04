import numpy as np


def compute_discounted_return(rewards, gamma):
    """
    Compute the discounted return from a sequence of rewards.

    Args:
        rewards: array-like of shape (T,) with reward at each step
        gamma: discount factor in [0, 1]

    Returns:
        float: discounted return G = sum(gamma^k * rewards[k])
    """
    rewards = np.asarray(rewards)
    powers = np.arange(len(rewards))
    discounts = gamma ** powers
    return float(np.sum(rewards * discounts))
