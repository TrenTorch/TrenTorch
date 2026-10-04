import numpy as np


def dpo_implicit_reward(pi_logp, ref_logp, beta):
    return beta * (np.asarray(pi_logp, dtype=float) - np.asarray(ref_logp, dtype=float))


def dpo_loss(pi_chosen, pi_rejected, ref_chosen, ref_rejected, beta):
    d = dpo_implicit_reward(pi_chosen, ref_chosen, beta) - dpo_implicit_reward(pi_rejected, ref_rejected, beta)
    return float(np.logaddexp(0.0, -d).mean())
