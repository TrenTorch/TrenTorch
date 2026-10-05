import numpy as np


def missingness_rate_by_group(x: np.ndarray, groups: np.ndarray) -> dict:
    x = np.asarray(x, dtype=float)
    groups = np.asarray(groups)
    missing = np.isnan(x)
    return {label: float(missing[groups == label].mean()) for label in np.unique(groups)}


def mean_by_missingness(target: np.ndarray, other: np.ndarray) -> tuple:
    missing = np.isnan(np.asarray(target, dtype=float))
    other = np.asarray(other, dtype=float)
    observed_mean = float(other[~missing].mean()) if (~missing).any() else float("nan")
    missing_mean = float(other[missing].mean()) if missing.any() else float("nan")
    return observed_mean, missing_mean


def likely_mechanism(target: np.ndarray, other: np.ndarray, threshold: float = 0.2) -> str:
    other = np.asarray(other, dtype=float)
    if not np.isnan(np.asarray(target, dtype=float)).any():
        return "MCAR-like"
    spread = other.std()
    if spread == 0.0:
        return "MCAR-like"
    observed_mean, missing_mean = mean_by_missingness(target, other)
    gap = abs(observed_mean - missing_mean) / spread
    return "MAR-like" if gap >= threshold else "MCAR-like"


def add_missing_indicators(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    mask = np.isnan(x)
    gappy = mask.any(axis=0)
    return np.hstack([x, mask[:, gappy].astype(float)])
