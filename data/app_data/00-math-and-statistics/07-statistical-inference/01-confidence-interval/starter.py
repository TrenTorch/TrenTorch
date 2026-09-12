import numpy as np
from scipy import stats


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
                     (stats.t.ppf((1 + confidence) / 2, df=n-1))
        margin     = t_critical * standard_error_of_mean(x)

    Returns (mean - margin, mean + margin).
    """
    pass
