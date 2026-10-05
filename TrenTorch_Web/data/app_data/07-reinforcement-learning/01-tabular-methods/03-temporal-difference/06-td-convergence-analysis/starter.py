import numpy as np


def td_convergence_analysis(episodes, true_values, gamma, alpha):
    """
    Analyze TD(0) convergence.

    Args:
        episodes: list of episodes, each is a list of (state, reward, next_state) tuples
        true_values: dict {state: true_value}
        gamma: discount factor
        alpha: learning rate

    Returns:
        V_estimates: dict {state: estimated_value}
        mse_per_episode: list of MSE values after each episode
    """
    pass
