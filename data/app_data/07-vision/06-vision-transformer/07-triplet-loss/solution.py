import numpy as np


def triplet_loss(anchor: np.ndarray, positive: np.ndarray, negative: np.ndarray, margin: float = 1.0) -> float:
    dist_pos = np.linalg.norm(anchor - positive, axis=1)
    dist_neg = np.linalg.norm(anchor - negative, axis=1)
    per_sample_loss = np.maximum(0.0, dist_pos - dist_neg + margin)
    return float(np.mean(per_sample_loss))
