import numpy as np


def _valid(lengths, T):
    return np.arange(T)[None, :] < np.asarray(lengths)[:, None]


def kl_penalized_rewards(logp_policy, logp_ref, final_reward, lengths, beta):
    lp, lr = np.asarray(logp_policy, float), np.asarray(logp_ref, float)
    B, T = lp.shape
    mask = _valid(lengths, T)
    rewards = -beta * (lp - lr) * mask
    rewards[np.arange(B), np.asarray(lengths) - 1] += np.asarray(final_reward, float)
    return rewards


def mean_kl(logp_policy, logp_ref, lengths):
    lp, lr = np.asarray(logp_policy, float), np.asarray(logp_ref, float)
    mask = _valid(lengths, lp.shape[1])
    return float(((lp - lr) * mask).sum() / mask.sum())
