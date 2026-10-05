import numpy as np


def compute_gae(values, rewards, next_values, gamma=0.99, lambda_=0.95):
    """
    Generalized Advantage Estimation.

    Args:
        values: critic values at each state
        rewards: rewards collected
        next_values: critic values at next states
        gamma: discount factor
        lambda_: GAE parameter [0,1]

    Returns:
        advantages: estimated advantages for each timestep
    """
    pass
