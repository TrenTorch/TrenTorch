import numpy as np


def td_residuals(rewards, values, gamma, last_value):
    """
    rewards: reward at each step, shape (T,)
    values: value estimate V(s_t) at each step, shape (T,)
    gamma: discount factor
    last_value: value estimate of the state after the final step

    Returns:
        delta_t = r_t + gamma * V(s_{t+1}) - V(s_t) for each step, shape (T,).
    """
    # TODO: Compute the one-step TD residual at every step (see Theory).
    pass
