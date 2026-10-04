import numpy as np


def group_advantages(rewards, eps=1e-6):
    r = np.asarray(rewards, dtype=float)
    mean = r.mean(axis=1, keepdims=True)
    std = r.std(axis=1, keepdims=True)
    return (r - mean) / (std + eps)


def clipped_surrogate_loss(ratio, advantage, clip_eps):
    ratio = np.asarray(ratio, dtype=float)
    adv = np.asarray(advantage, dtype=float)
    unclipped = ratio * adv
    clipped = np.clip(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * adv
    return float(-np.minimum(unclipped, clipped).mean())
