import numpy as np


def replace_where(a: np.ndarray, mask: np.ndarray, value) -> np.ndarray:
    return np.where(mask, value, a)


def clip_to_percentiles(a: np.ndarray, low: float, high: float) -> np.ndarray:
    lo, hi = np.percentile(a, [low, high])
    return np.clip(a, lo, hi)


def sign_class(a: np.ndarray) -> np.ndarray:
    return np.select([a < 0, a == 0], [-1, 0], default=1)


def bucket_label(a: np.ndarray, low: float, high: float) -> np.ndarray:
    return np.select([a < low, a >= high], ["low", "high"], default="mid")
