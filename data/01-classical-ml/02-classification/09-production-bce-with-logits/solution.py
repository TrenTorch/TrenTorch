import numpy as np


def bce_with_logits_loss(z: np.ndarray, y: np.ndarray) -> float:
    max_z_zero = np.maximum(z, 0)
    stable_log_term = np.log1p(np.exp(-np.abs(z)))
    per_sample = max_z_zero - z * y + stable_log_term
    return float(np.mean(per_sample))
