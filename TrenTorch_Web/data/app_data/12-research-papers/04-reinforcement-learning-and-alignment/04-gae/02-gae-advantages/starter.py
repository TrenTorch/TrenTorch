import numpy as np


def gae_advantages(deltas, gamma, lam):
    """
    deltas: one-step TD residuals, shape (T,)
    gamma: discount factor
    lam: GAE smoothing parameter in [0, 1]

    Returns:
        A_t = sum_k (gamma * lam)^k * delta_{t+k}, computed backward, shape (T,).
    """
    # TODO: Run the backward recursion A_t = delta_t + gamma * lam * A_{t+1} (see Theory).
    pass
