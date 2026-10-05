import numpy as np


def policy_gradient_loss(log_probs, advantages):
    """
    Policy gradient loss.

    Args:
        log_probs: log probabilities of actions
        advantages: advantage estimates (reward - baseline)

    Returns:
        loss: scalar (negative, for gradient ascent)
    """
    log_probs = np.array(log_probs, dtype=np.float32)
    advantages = np.array(advantages, dtype=np.float32)

    # Policy gradient: -E[log π(a|s) * advantage]
    loss = -np.mean(log_probs * advantages)

    return float(loss)
