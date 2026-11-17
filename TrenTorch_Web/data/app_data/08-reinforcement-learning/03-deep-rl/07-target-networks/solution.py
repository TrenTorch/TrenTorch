import numpy as np


def soft_update_target_network(params_main, params_target, tau=0.001):
    """
    Soft update target network parameters.

    Args:
        params_main: main network parameters
        params_target: target network parameters
        tau: soft update coefficient [0, 1]

    Returns:
        updated params_target
    """
    params_main = np.array(params_main, dtype=np.float32)
    params_target = np.array(params_target, dtype=np.float32)

    # Soft update: target = (1 - tau) * target + tau * main
    updated_target = (1.0 - tau) * params_target + tau * params_main

    return updated_target
