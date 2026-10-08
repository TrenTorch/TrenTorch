import numpy as np


def discounted_returns(rewards, gamma):
    rewards = np.asarray(rewards, dtype=float)
    out = np.zeros_like(rewards)
    G = 0.0
    for t in reversed(range(len(rewards))):
        G = rewards[t] + gamma * G
        out[t] = G
    return out
