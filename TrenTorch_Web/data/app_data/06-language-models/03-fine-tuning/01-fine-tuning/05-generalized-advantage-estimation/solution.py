import numpy as np


def td_residuals(rewards: np.ndarray, values: np.ndarray, next_values: np.ndarray, dones: np.ndarray, gamma: float) -> np.ndarray:
    rewards = np.asarray(rewards, dtype=float)
    values = np.asarray(values, dtype=float)
    next_values = np.asarray(next_values, dtype=float)
    dones = np.asarray(dones, dtype=float)
    return rewards + gamma * next_values * (1 - dones) - values


def generalized_advantage_estimation(
    rewards: np.ndarray, values: np.ndarray, next_values: np.ndarray, dones: np.ndarray, gamma: float, lam: float
) -> np.ndarray:
    deltas = td_residuals(rewards, values, next_values, dones, gamma)
    dones = np.asarray(dones, dtype=float)
    T = len(rewards)
    advantages = np.zeros(T)
    running = 0.0
    for t in reversed(range(T)):
        running = deltas[t] + gamma * lam * (1 - dones[t]) * running
        advantages[t] = running
    return advantages
