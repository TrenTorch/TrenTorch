import numpy as np


def actor_critic_loss(policy_logprobs, actions, rewards, next_values, gamma=0.99):
    """
    Compute actor-critic losses.

    Args:
        policy_logprobs: log probabilities of taken actions
        actions: actions actually taken
        rewards: immediate rewards
        next_values: value estimates of next states
        gamma: discount factor

    Returns:
        actor_loss: scalar loss for policy
        critic_loss: scalar loss for value
    """
    pass
