import numpy as np


def logit_lens(resid, W_U, norm_weight, eps=1e-6):
    x = np.asarray(resid, dtype=float)
    rms = np.sqrt(np.mean(x ** 2, axis=1, keepdims=True) + eps)
    return (x / rms * norm_weight) @ W_U


def target_rank_by_layer(logits, target):
    return (logits > logits[:, [target]]).sum(axis=1)
