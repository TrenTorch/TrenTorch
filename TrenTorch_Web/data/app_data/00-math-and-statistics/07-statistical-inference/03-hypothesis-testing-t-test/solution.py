import math

import numpy as np


def _regularized_incomplete_beta(x: float, a: float, b: float) -> float:
    """
    I_x(a, b), computed via the continued-fraction expansion (the
    standard numerical-recipes approach): the piece scipy.stats.t.cdf
    is built on internally, needed here since only numpy (not scipy)
    is available at runtime.
    """
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0

    def betacf(a: float, b: float, x: float) -> float:
        qab, qap, qam = a + b, a + 1.0, a - 1.0
        c = 1.0
        d = 1.0 - qab * x / qap
        d = 1e-30 if abs(d) < 1e-30 else d
        d = 1.0 / d
        h = d
        for m in range(1, 201):
            m2 = 2 * m
            aa = m * (b - m) * x / ((qam + m2) * (a + m2))
            d = 1.0 + aa * d
            d = 1e-30 if abs(d) < 1e-30 else d
            c = 1.0 + aa / c
            c = 1e-30 if abs(c) < 1e-30 else c
            d = 1.0 / d
            h *= d * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
            d = 1.0 + aa * d
            d = 1e-30 if abs(d) < 1e-30 else d
            c = 1.0 + aa / c
            c = 1e-30 if abs(c) < 1e-30 else c
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1.0) < 1e-12:
                break
        return h

    front = math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return front * betacf(a, b, x) / a
    return 1.0 - front * betacf(b, a, 1.0 - x) / b


def _t_cdf(t: float, df: float) -> float:
    """Student's t-distribution CDF, via the regularized incomplete beta."""
    x = df / (df + t * t)
    ib = _regularized_incomplete_beta(x, df / 2.0, 0.5)
    return 1.0 - 0.5 * ib if t >= 0 else 0.5 * ib


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
    p_value = 2.0 * (1.0 - _t_cdf(abs(t_statistic), df))
    return t_statistic, float(p_value)
