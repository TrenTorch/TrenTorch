import numpy as np


def running_total(a: np.ndarray) -> np.ndarray:
    return np.cumsum(a)


def cumulative_max(a: np.ndarray) -> np.ndarray:
    return np.maximum.accumulate(a)


def consecutive_differences(a: np.ndarray) -> np.ndarray:
    return np.diff(a)


def percent_change(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    previous = a[:-1]
    change = np.full(previous.shape, np.nan)
    np.divide(np.diff(a), previous, out=change, where=previous != 0)
    return change


def moving_average(a: np.ndarray, w: int) -> np.ndarray:
    c = np.concatenate(([0.0], np.cumsum(np.asarray(a, dtype=float))))
    return (c[w:] - c[:-w]) / w
