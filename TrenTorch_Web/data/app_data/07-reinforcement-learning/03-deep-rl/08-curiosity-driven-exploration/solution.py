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
    next_state = np.array(next_state, dtype=np.float32)
    predicted_next = np.array(predicted_next, dtype=np.float32)

    # Prediction error is intrinsic reward
    error = next_state - predicted_next
    prediction_error = np.sum(error ** 2)  # L2 error

    # Intrinsic reward = curiosity_strength * prediction_error
    intrinsic_reward = curiosity_strength * prediction_error

    return float(intrinsic_reward)
