import numpy as np


def behavioral_cloning_loss(policy_logits, expert_actions):
    """
    Behavioral cloning loss.

    Args:
        policy_logits: predicted action logits (batch_size, num_actions)
        expert_actions: expert action indices (batch_size,)

    Returns:
        loss: scalar cross-entropy loss
    """
    pass
