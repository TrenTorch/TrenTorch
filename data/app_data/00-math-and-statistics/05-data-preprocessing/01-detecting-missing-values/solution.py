import numpy as np


def missing_mask(x: np.ndarray) -> np.ndarray:
    return np.isnan(x)


def missing_count_per_column(x: np.ndarray) -> np.ndarray:
    return missing_mask(x).sum(axis=0)


def missing_fraction_per_column(x: np.ndarray) -> np.ndarray:
    return missing_count_per_column(x) / x.shape[0]
