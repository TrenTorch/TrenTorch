import numpy as np


def actor_critic_losses(log_probs, values, actions, rewards, next_values, gamma, clip_ratio=None):
    """
    Compute actor-critic losses.

    Args:
        log_probs: log probabilities of actions
        values: critic value predictions
        actions: actions taken
        rewards: immediate rewards
        next_values: critic values of next states
        gamma: discount factor
        clip_ratio: optional PPO clipping ratio

    Returns:
        actor_loss, critic_loss: scalar losses
    """
    pass
