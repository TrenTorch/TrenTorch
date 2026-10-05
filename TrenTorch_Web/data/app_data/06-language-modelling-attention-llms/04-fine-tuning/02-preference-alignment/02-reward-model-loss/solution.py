import numpy as np


def reward_model_loss(r_chosen, r_rejected):
    d = np.asarray(r_chosen, dtype=float) - np.asarray(r_rejected, dtype=float)
    return float(np.logaddexp(0.0, -d).mean())


def preference_accuracy(r_chosen, r_rejected):
    return float((np.asarray(r_chosen) > np.asarray(r_rejected)).mean())
