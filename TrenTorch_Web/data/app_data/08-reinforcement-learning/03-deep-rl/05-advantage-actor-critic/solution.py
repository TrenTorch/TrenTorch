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
    log_probs = np.array(log_probs, dtype=np.float32)
    values = np.array(values, dtype=np.float32)
    next_values = np.array(next_values, dtype=np.float32)
    rewards = np.array(rewards, dtype=np.float32)

    # TD targets and advantages
    td_targets = rewards + gamma * next_values
    advantages = td_targets - values

    # Actor loss with entropy regularization
    actor_loss = -np.mean(log_probs * advantages)

    # Entropy: -E[log p] (already have log probs)
    entropy = -np.mean(log_probs)

    # Critic loss
    critic_loss = np.mean(advantages ** 2)

    # Total actor loss includes entropy bonus
    actor_loss = actor_loss - entropy_coeff * entropy

    return float(actor_loss), float(critic_loss), float(entropy)
