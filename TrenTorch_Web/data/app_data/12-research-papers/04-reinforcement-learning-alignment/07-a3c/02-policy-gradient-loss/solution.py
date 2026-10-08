import numpy as np


def policy_gradient_loss(logp, adv):
    return float(-np.mean(np.asarray(logp, dtype=float) * np.asarray(adv, dtype=float)))
