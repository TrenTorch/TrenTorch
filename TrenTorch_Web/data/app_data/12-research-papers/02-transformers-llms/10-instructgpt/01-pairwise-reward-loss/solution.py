import numpy as np


def pairwise_reward_loss(r_chosen, r_rejected):
    return np.logaddexp(0.0, -(np.asarray(r_chosen, dtype=float) - np.asarray(r_rejected, dtype=float)))
