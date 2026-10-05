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
    pass
