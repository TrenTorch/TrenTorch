import numpy as np


def per_token_kl(logp_policy, logp_ref):
    return float(np.sum(np.asarray(logp_policy, dtype=float) - np.asarray(logp_ref, dtype=float)))
