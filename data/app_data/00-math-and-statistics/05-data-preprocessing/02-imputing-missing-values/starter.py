import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

missing_mask = load_solution(
    "00-math-and-statistics/05-data-preprocessing/01-detecting-missing-values"
).missing_mask


def impute_with_mean(x: np.ndarray) -> np.ndarray:
    """
    Replace every missing (NaN) value with its OWN COLUMN's mean,
    computed from that column's non-missing values only
    (np.nanmean ignores NaNs automatically, rather than propagating
    them into the mean itself).

    Must not mutate the input array, work on a copy.
    """
    pass


def impute_with_median(x: np.ndarray) -> np.ndarray:
    """
    Same idea as impute_with_mean, but replacing with each column's
    median (np.nanmedian) instead. See Theory for why median is
    sometimes the better choice.
    """
    pass
