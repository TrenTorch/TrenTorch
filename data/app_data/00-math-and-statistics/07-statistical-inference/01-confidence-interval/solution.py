import numpy as np
from scipy import stats


def standard_error_of_mean(x: np.ndarray) -> float:
    return float(np.std(x, ddof=1) / np.sqrt(len(x)))


def confidence_interval_mean(x: np.ndarray, confidence: float = 0.95) -> tuple[float, float]:
    n = len(x)
    mean = float(np.mean(x))
    sem = standard_error_of_mean(x)
    t_critical = stats.t.ppf((1.0 + confidence) / 2.0, df=n - 1)
    margin = t_critical * sem
    return mean - margin, mean + margin
