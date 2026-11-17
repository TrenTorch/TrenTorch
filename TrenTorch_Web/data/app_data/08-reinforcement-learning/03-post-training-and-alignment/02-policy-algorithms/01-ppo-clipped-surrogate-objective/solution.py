import numpy as np


def probability_ratio(new_log_prob: np.ndarray, old_log_prob: np.ndarray) -> np.ndarray:
    return np.exp(new_log_prob - old_log_prob)


def ppo_clipped_surrogate_loss(ratio: np.ndarray, advantage: np.ndarray, epsilon: float = 0.2) -> np.ndarray:
    unclipped = ratio * advantage
    clipped = np.clip(ratio, 1 - epsilon, 1 + epsilon) * advantage
    return -np.minimum(unclipped, clipped)


def fraction_of_ratios_clipped(ratio: np.ndarray, epsilon: float = 0.2) -> float:
    return float(np.mean((ratio < 1 - epsilon) | (ratio > 1 + epsilon)))
