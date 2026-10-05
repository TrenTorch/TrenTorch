import numpy as np


def grpo_group_relative_advantage(rewards: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    """
    GRPO's core trick (DeepSeekMath, Shao et al. 2024): instead of
    training a separate value network to estimate a baseline (like
    Generalized Advantage Estimation does), sample a GROUP of several
    responses to the SAME prompt, score each with the reward model,
    and normalize within that group: (reward - group_mean) /
    group_std. A response's advantage is purely relative to its
    siblings.
    """
    # TODO: convert rewards to a float array, then return
    # (rewards - rewards.mean()) / (rewards.std() + eps)
    pass


def grpo_policy_gradient_loss(log_probs: np.ndarray, advantages: np.ndarray) -> float:
    """
    The standard policy-gradient loss, using GRPO's group-relative
    advantage in place of a value-network-based one:
    -mean(log_prob * advantage) -- pushes up the log-probability of
    responses with above-group-average reward, pushes down the
    log-probability of below-average ones.
    """
    # TODO: -np.mean(log_probs * advantages)
    pass
