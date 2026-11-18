import numpy as np


def apply_penalties(logits, generated_ids, rep=1.0, freq=0.0, pres=0.0):
    out = np.array(logits, dtype=float, copy=True)
    counts = np.bincount(np.asarray(generated_ids, dtype=int), minlength=len(out)) if len(generated_ids) else np.zeros(len(out), int)
    seen = counts > 0
    out[seen & (out > 0)] /= rep
    out[seen & (out <= 0)] *= rep
    out[seen] -= freq * counts[seen] + pres
    return out
