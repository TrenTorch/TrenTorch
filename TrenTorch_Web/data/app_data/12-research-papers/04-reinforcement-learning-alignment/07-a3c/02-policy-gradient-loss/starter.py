import numpy as np


def policy_gradient_loss(logp, adv):
    """
    logp: log-probability of each sampled action under the policy, shape (N,)
    adv: advantage estimate for each action, shape (N,)

    Returns:
        -mean(logp * adv), the policy-gradient loss, as a float.
    """
    # TODO: Multiply each log-probability by its advantage, average, and negate (see Theory).
    pass
