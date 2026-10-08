import numpy as np


def dpo_loss(logit):
    return np.logaddexp(0.0, -np.asarray(logit, dtype=float))
