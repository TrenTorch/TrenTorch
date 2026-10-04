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
    policy_logprobs = np.array(policy_logprobs, dtype=np.float32)
    rewards = np.array(rewards, dtype=np.float32)
    next_values = np.array(next_values, dtype=np.float32)

    # Compute advantages
    advantages = rewards + gamma * next_values

    # Actor loss: negative log prob times advantage
    actor_loss = -np.mean(policy_logprobs * advantages)

    # Critic loss: MSE of value prediction
    critic_loss = np.mean(advantages ** 2)

    return float(actor_loss), float(critic_loss)
