
import numpy as np

from _load import load_solution

missing_mask = load_solution("math-detecting-missing-values").missing_mask


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
