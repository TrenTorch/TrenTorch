import numpy as np


def compute_curiosity_reward(state, action, next_state, predicted_next, curiosity_strength=1.0):
    """
    Compute intrinsic curiosity reward.

    Args:
        state: current state
        action: action taken
        next_state: actual next state
        predicted_next: predicted next state from forward model
        curiosity_strength: scaling factor for intrinsic reward

    Returns:
        intrinsic_reward: scalar curiosity bonus
    """
    pass
