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
    log_probs = np.array(log_probs, dtype=np.float32)
    values = np.array(values, dtype=np.float32)
    rewards = np.array(rewards, dtype=np.float32)
    next_values = np.array(next_values, dtype=np.float32)

    # Compute advantages
    td_targets = rewards + gamma * next_values
    advantages = td_targets - values

    # Actor loss: -log π(a|s) * advantage
    actor_loss = -np.mean(log_probs * advantages)

    # Critic loss: MSE of value prediction
    critic_loss = np.mean(advantages ** 2)

    return float(actor_loss), float(critic_loss)
