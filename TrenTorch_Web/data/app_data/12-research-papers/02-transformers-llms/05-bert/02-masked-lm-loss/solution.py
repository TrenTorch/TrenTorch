import numpy as np


def masked_lm_loss(log_probs, targets, mask):
    log_probs = np.asarray(log_probs, dtype=float)
    nll = -log_probs[np.arange(len(targets)), targets]
    m = np.asarray(mask, dtype=bool)
    if not m.any():
        return 0.0
    return float(nll[m].mean())
