import numpy as np


def linear_td_update(w, phi, reward, next_phi, gamma, alpha):
    """
    Linear TD update.

    Args:
        w: weight vector
        phi: feature vector for current state
        reward: immediate reward
        next_phi: feature vector for next state
        gamma: discount factor
        alpha: learning rate

    Returns:
        w_updated: updated weight vector
    """
    phi = np.array(phi, dtype=np.float32)
    next_phi = np.array(next_phi, dtype=np.float32)
    w = np.array(w, dtype=np.float32)

    # Current and next state values
    v_s = np.dot(w, phi)
    v_next = np.dot(w, next_phi)

    # TD error
    td_error = reward + gamma * v_next - v_s

    # Update weights
    w_updated = w + alpha * td_error * phi

    return w_updated
