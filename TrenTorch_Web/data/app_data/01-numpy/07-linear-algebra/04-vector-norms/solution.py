import numpy as np


def l2_norm_from_scratch(v: np.ndarray) -> float:
    return np.sqrt(np.sum(v**2))


def l2_norm_builtin(v: np.ndarray) -> float:
    return np.linalg.norm(v)


def normalize_vector(v: np.ndarray) -> np.ndarray:
    return v / np.linalg.norm(v)
