import numpy as np


def dyna_backup(rewards, values, gamma=0.99):
    """
    Dyna Q-learning backup combining real and imagined updates.

    Args:
        rewards: real and imagined rewards
        values: bootstrapped values for next states
        gamma: discount factor

    Returns:
        targets: TD targets for value updates
    """
    rewards = np.array(rewards, dtype=np.float32)
    values = np.array(values, dtype=np.float32)

    # TD targets: r + γV(s')
    targets = rewards + gamma * values

    return targets
