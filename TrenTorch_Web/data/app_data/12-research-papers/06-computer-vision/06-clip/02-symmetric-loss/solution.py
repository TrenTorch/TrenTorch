import numpy as np


def clip_symmetric_loss(logits):
    logits = np.asarray(logits, dtype=float)

    def ce(L):
        return float(np.mean(np.logaddexp.reduce(L, axis=1) - np.diag(L)))

    return (ce(logits) + ce(logits.T)) / 2
