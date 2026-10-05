import numpy as np


def summary_ignoring_nan(a: np.ndarray) -> dict:
    known = a[~np.isnan(a)]
    if known.size == 0:
        nan = float("nan")
        return {"count": 0, "mean": nan, "std": nan, "min": nan, "max": nan}
    return {
        "count": int(known.size),
        "mean": float(np.mean(known)),
        "std": float(np.std(known)),
        "min": float(np.min(known)),
        "max": float(np.max(known)),
    }


def count_missing(m: np.ndarray, axis: int) -> np.ndarray:
    return np.isnan(m).sum(axis=axis)


def fill_with_column_means(m: np.ndarray) -> np.ndarray:
    out = np.array(m, dtype=float, copy=True)
    holes = np.isnan(out)
    known_count = (~holes).sum(axis=0)
    column_sum = np.where(holes, 0.0, out).sum(axis=0)
    means = np.divide(column_sum, known_count, out=np.zeros(out.shape[1]), where=known_count > 0)
    rows, cols = np.nonzero(holes)
    out[rows, cols] = means[cols]
    return out


def rows_without_nan(m: np.ndarray) -> np.ndarray:
    return m[~np.isnan(m).any(axis=1)]


def argmax_ignoring_nan(a: np.ndarray) -> int:
    if np.isnan(a).all():
        return -1
    return int(np.nanargmax(a))
