import numpy as np


def compute_gae(values, rewards, next_values, gamma=0.99, lambda_=0.95):
    """
    Generalized Advantage Estimation.

    Args:
        values: critic values at each state
        rewards: rewards collected
        next_values: critic values at next states
        gamma: discount factor
        lambda_: GAE parameter [0,1]

    Returns:
        advantages: estimated advantages for each timestep
    """
    values = np.array(values, dtype=np.float32)
    rewards = np.array(rewards, dtype=np.float32)
    next_values = np.array(next_values, dtype=np.float32)

    T = len(rewards)
    gae = np.zeros(T, dtype=np.float32)

    # TD residuals
    deltas = rewards + gamma * next_values - values

    # Backward pass: compute GAE from end of trajectory
    cumulative = 0.0
    for t in range(T - 1, -1, -1):
        cumulative = deltas[t] + gamma * lambda_ * cumulative
        gae[t] = cumulative

    return gae
