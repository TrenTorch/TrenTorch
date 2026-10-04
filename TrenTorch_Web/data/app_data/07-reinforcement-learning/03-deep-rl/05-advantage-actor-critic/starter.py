import numpy as np


def a3c_losses(log_probs, values, next_values, actions, rewards, gamma, entropy_coeff=0.01):
    """
    A3C worker losses.

    Args:
        log_probs: log probabilities of actions
        values: critic value predictions
        next_values: critic values of next states
        actions: actions taken
        rewards: immediate rewards
        gamma: discount factor
        entropy_coeff: entropy regularization coefficient

    Returns:
        actor_loss, critic_loss, entropy: scalars
    """
    pass
