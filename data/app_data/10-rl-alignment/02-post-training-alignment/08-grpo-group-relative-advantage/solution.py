import numpy as np


def grpo_group_relative_advantage(rewards: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    rewards = np.asarray(rewards, dtype=float)
    return (rewards - rewards.mean()) / (rewards.std() + eps)


def grpo_policy_gradient_loss(log_probs: np.ndarray, advantages: np.ndarray) -> float:
    return float(-np.mean(log_probs * advantages))
