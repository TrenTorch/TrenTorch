import numpy as np


def ppo_objective(ratios, advantages, eps):
    ratios = np.asarray(ratios, dtype=float)
    advantages = np.asarray(advantages, dtype=float)
    clipped = np.clip(ratios, 1 - eps, 1 + eps)
    return float(np.mean(np.minimum(ratios * advantages, clipped * advantages)))
