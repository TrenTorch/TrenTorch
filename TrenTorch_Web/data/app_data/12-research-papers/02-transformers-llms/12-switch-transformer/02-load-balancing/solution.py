import numpy as np


def load_balancing_loss(expert_index, probs, n_experts):
    T = len(expert_index)
    f = np.bincount(expert_index, minlength=n_experts) / T
    P = probs.mean(axis=0)
    return float(n_experts * np.sum(f * P))
