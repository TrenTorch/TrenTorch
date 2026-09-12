import numpy as np
from scipy import stats


def welch_t_statistic(a: np.ndarray, b: np.ndarray) -> float:
    mean_a, mean_b = np.mean(a), np.mean(b)
    var_a, var_b = np.var(a, ddof=1), np.var(b, ddof=1)
    n_a, n_b = len(a), len(b)
    standard_error = np.sqrt(var_a / n_a + var_b / n_b)
    return float((mean_a - mean_b) / standard_error)


def welch_degrees_of_freedom(a: np.ndarray, b: np.ndarray) -> float:
    var_a, var_b = np.var(a, ddof=1), np.var(b, ddof=1)
    n_a, n_b = len(a), len(b)
    numerator = (var_a / n_a + var_b / n_b) ** 2
    denominator = (var_a / n_a) ** 2 / (n_a - 1) + (var_b / n_b) ** 2 / (n_b - 1)
    return float(numerator / denominator)


def two_sample_t_test(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    t_statistic = welch_t_statistic(a, b)
    df = welch_degrees_of_freedom(a, b)
    p_value = 2.0 * (1.0 - stats.t.cdf(abs(t_statistic), df))
    return t_statistic, float(p_value)
