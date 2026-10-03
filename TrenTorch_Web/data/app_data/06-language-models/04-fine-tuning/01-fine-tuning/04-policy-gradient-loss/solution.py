import numpy as np


def discounted_returns(rewards: np.ndarray, gamma: float, dones: np.ndarray) -> np.ndarray:
    rewards = np.asarray(rewards, dtype=float)
    dones = np.asarray(dones, dtype=float)
    T = len(rewards)
    returns = np.zeros(T)
    running = 0.0
    for t in reversed(range(T)):
        running = rewards[t] + gamma * (1 - dones[t]) * running
        returns[t] = running
    return returns


def policy_gradient_loss(log_probs: np.ndarray, advantages: np.ndarray) -> float:
    return float(-np.mean(log_probs * advantages))
