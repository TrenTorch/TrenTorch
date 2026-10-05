import numpy as np


def prioritized_replay_buffer(transitions, td_errors, batch_size, alpha=0.6, epsilon=1e-6):
    """
    Prioritized experience replay buffer.

    Args:
        transitions: list of (s, a, r, s', done) tuples
        td_errors: list of absolute TD-error for each transition
        batch_size: size of batch to sample
        alpha: priority exponent (0=uniform, 1=greedy)
        epsilon: small constant to avoid zero priorities

    Returns:
        indices: array of sampled transition indices
    """
    pass
