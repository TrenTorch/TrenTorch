import numpy as np


def discounted_returns(rewards, gamma):
    """
    rewards: rewards in time order, shape (T,)
    gamma: discount factor

    Returns:
        G_t = r_t + gamma * G_{t+1}, the discounted return from each step, shape (T,).
    """
    # TODO: Accumulate the discounted return backward from the last step (see Theory).
    pass
