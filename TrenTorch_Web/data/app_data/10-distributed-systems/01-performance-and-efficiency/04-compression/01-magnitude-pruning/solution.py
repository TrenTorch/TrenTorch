import numpy as np


def magnitude_prune(weight: np.ndarray, sparsity: float) -> np.ndarray:
    if sparsity <= 0.0:
        return weight.copy()

    flat_abs = np.abs(weight).flatten()
    num_to_prune = int(np.floor(sparsity * flat_abs.size))
    if num_to_prune == 0:
        return weight.copy()

    threshold = np.partition(flat_abs, num_to_prune - 1)[num_to_prune - 1]
    mask = np.abs(weight) > threshold
    return weight * mask
