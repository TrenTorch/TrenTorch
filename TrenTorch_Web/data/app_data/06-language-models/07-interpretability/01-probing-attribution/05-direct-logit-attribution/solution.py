import numpy as np


def direct_logit_attribution(components, W_U, correct, wrong, scale):
    direction = W_U[:, correct] - W_U[:, wrong]
    return (np.asarray(components, dtype=float) @ direction) / scale


def attribution_total(contributions):
    return float(np.sum(contributions))
