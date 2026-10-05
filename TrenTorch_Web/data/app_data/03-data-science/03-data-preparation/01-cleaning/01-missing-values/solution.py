import numpy as np


def missing_mask(x: np.ndarray) -> np.ndarray:
    return np.isnan(x)


def missing_count_per_column(x: np.ndarray) -> np.ndarray:
    return missing_mask(x).sum(axis=0)


def missing_fraction_per_column(x: np.ndarray) -> np.ndarray:
    return missing_count_per_column(x) / x.shape[0]


def impute_with_mean(x: np.ndarray) -> np.ndarray:
    result = x.copy()
    column_means = np.nanmean(x, axis=0)
    mask = missing_mask(result)
    result[mask] = np.take(column_means, np.where(mask)[1])
    return result


def impute_with_median(x: np.ndarray) -> np.ndarray:
    result = x.copy()
    column_medians = np.nanmedian(x, axis=0)
    mask = missing_mask(result)
    result[mask] = np.take(column_medians, np.where(mask)[1])
    return result
