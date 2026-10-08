import numpy as np


def soft_target_ce(teacher_logits, student_logits, T):
    t = np.asarray(teacher_logits, dtype=float) / T
    s = np.asarray(student_logits, dtype=float) / T
    p = np.exp(t - t.max()) / np.exp(t - t.max()).sum()
    log_q = s - s.max() - np.log(np.exp(s - s.max()).sum())
    return float(-np.sum(p * log_q) * T**2)
