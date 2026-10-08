import numpy as np


def per_token_kl(logp_policy, logp_ref):
    """
    logp_policy: per-token log-probabilities under the policy, shape (T,)
    logp_ref: per-token log-probabilities of the same tokens under the reference model, shape (T,)

    Returns:
        The sampled estimate of KL divergence for the sequence: sum(logp_policy - logp_ref).
    """
    # TODO: Sum the per-token log-ratio over the sequence (see Theory).
    pass
