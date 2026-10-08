import numpy as np


def probability_ratio(logp_new, logp_old):
    """
    logp_new: log-probability of the action under the policy being trained
    logp_old: log-probability of the same action under the policy that collected the data

    Returns:
        r = pi_new / pi_old, computed as exp(logp_new - logp_old).
    """
    # TODO: Exponentiate the difference of the two log-probabilities (see Theory).
    pass
