import numpy as np

def solve(logits, target):
    logits = np.asarray(logits, dtype=float)
    maximum = np.max(logits)
    log_sum_exp = maximum + np.log(np.exp(logits - maximum).sum())
    return float(log_sum_exp - logits[int(target)])
