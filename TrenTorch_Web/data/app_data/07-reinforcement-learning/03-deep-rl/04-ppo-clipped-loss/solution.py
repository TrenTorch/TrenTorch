import numpy as np


def ppo_loss(log_probs_new, log_probs_old, advantages, epsilon=0.2):
    """
    PPO clipped loss.

    Args:
        log_probs_new: log probabilities under new policy
        log_probs_old: log probabilities under old policy
        advantages: computed advantages
        epsilon: clipping range [1-eps, 1+eps]

    Returns:
        scalar loss
    """
    log_probs_new = np.array(log_probs_new, dtype=np.float32)
    log_probs_old = np.array(log_probs_old, dtype=np.float32)
    advantages = np.array(advantages, dtype=np.float32)

    # Probability ratio
    ratio = np.exp(log_probs_new - log_probs_old)

    # Unclipped loss
    unclipped = ratio * advantages

    # Clipped loss
    clipped = np.clip(ratio, 1 - epsilon, 1 + epsilon) * advantages

    # PPO: take minimum, then negate
    loss = -np.mean(np.minimum(unclipped, clipped))

    return float(loss)
