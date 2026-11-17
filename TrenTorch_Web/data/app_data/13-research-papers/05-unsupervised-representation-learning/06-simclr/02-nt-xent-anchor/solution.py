import numpy as np


def nt_xent_anchor(sim_pos, sims_neg, tau):
    logits = np.concatenate([[sim_pos], np.asarray(sims_neg, dtype=float)]) / tau
    return float(np.logaddexp.reduce(logits) - logits[0])
