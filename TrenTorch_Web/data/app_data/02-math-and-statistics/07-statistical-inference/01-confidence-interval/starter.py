import math

import numpy as np


def _regularized_incomplete_beta(x: float, a: float, b: float) -> float:
    """
    I_x(a, b), computed via the continued-fraction expansion (the
    standard numerical-recipes approach): the piece scipy.stats.t.ppf
    is built on internally, needed here since only numpy (not scipy)
    is available at runtime. Provided as-is -- not something you need
    to implement, just a building block for confidence_interval_mean
    below.
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
    via bisection on _t_cdf. Provided as-is: use this in
    confidence_interval_mean below exactly like you would use
    scipy.stats.t.ppf(p, df=df).
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
    """
    The standard error of the mean: how much a SAMPLE MEAN is expected
    to vary from sample to sample, distinct from the standard
    deviation of the raw data itself.

        SEM = std(x, ddof=1) / sqrt(n)

    Uses the unbiased (ddof=1, Bessel-corrected) standard deviation,
    02-expectation-variance's own convention for estimating a
    population statistic from a sample.
    """
    pass


def confidence_interval_mean(x: np.ndarray, confidence: float = 0.95) -> tuple[float, float]:
    """
    A confidence interval for the TRUE population mean, given a sample
    x. Uses the t-distribution (appropriate for any sample size,
    especially small samples, where the Normal approximation used by a
    z-interval is unreliable):

        t_critical = t-distribution's critical value for this
                     confidence level, with (n - 1) degrees of freedom
                     (_t_ppf((1 + confidence) / 2, df=n-1))
        margin     = t_critical * standard_error_of_mean(x)

    Returns (mean - margin, mean + margin).
    """
    pass
