import math

import numpy as np


def _regularized_incomplete_beta(x: float, a: float, b: float) -> float:
    """
    I_x(a, b), computed via the continued-fraction expansion (the
    standard numerical-recipes approach): the piece scipy.stats.t.ppf
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


def _t_ppf(p: float, df: float) -> float:
    """
    Student's t-distribution's inverse CDF (percent point function),
    via bisection on _t_cdf -- there's no closed form, but _t_cdf is
    monotonic in t, so bisection converges to machine precision in a
    couple hundred iterations.
    """
    lo, hi = -1000.0, 1000.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if _t_cdf(mid, df) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def standard_error_of_mean(x: np.ndarray) -> float:
    return float(np.std(x, ddof=1) / np.sqrt(len(x)))


def confidence_interval_mean(x: np.ndarray, confidence: float = 0.95) -> tuple[float, float]:
    n = len(x)
    mean = float(np.mean(x))
    sem = standard_error_of_mean(x)
    t_critical = _t_ppf((1.0 + confidence) / 2.0, df=n - 1)
    margin = t_critical * sem
    return mean - margin, mean + margin
