import math

import numpy as np


def _normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def normal_ppf(p: float) -> float:
    if not 0.0 < p < 1.0:
        raise ValueError("p must be strictly between 0 and 1")
    low, high = -40.0, 40.0
    for _ in range(200):
        mid = 0.5 * (low + high)
        if _normal_cdf(mid) < p:
            low = mid
        else:
            high = mid
    return float(0.5 * (low + high))


def plotting_positions(n: int) -> np.ndarray:
    return (np.arange(1, n + 1) - 0.5) / n


def qq_points(x: np.ndarray) -> tuple:
    sample = np.sort(np.asarray(x, dtype=float))
    theoretical = np.array([normal_ppf(p) for p in plotting_positions(len(sample))])
    return theoretical, sample


def qq_line(theoretical: np.ndarray, sample: np.ndarray) -> tuple:
    t25, t75 = np.percentile(theoretical, [25, 75])
    s25, s75 = np.percentile(sample, [25, 75])
    slope = (s75 - s25) / (t75 - t25)
    return float(slope), float(s25 - slope * t25)


def qq_correlation(x: np.ndarray) -> float:
    theoretical, sample = qq_points(x)
    return float(np.corrcoef(theoretical, sample)[0, 1])
