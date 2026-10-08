import numpy as np


def td_residuals(rewards, values, gamma, last_value):
    rewards = np.asarray(rewards, dtype=float)
    values = np.asarray(values, dtype=float)
    next_values = np.append(values[1:], last_value)
    return rewards + gamma * next_values - values
