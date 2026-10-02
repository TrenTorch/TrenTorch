import numpy as np


def sample_mean(x: np.ndarray) -> float:
    return float(np.mean(x))


def sample_variance(x: np.ndarray, ddof: int = 0) -> float:
    return float(np.var(x, ddof=ddof))
