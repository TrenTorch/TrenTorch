import numpy as np
from scipy import stats


def welch_t_statistic(a: np.ndarray, b: np.ndarray) -> float:
    """
    Welch's t-statistic: measures how many standard errors apart the
    two sample means are, WITHOUT assuming the two groups have equal
    variance (the more robust, more commonly-recommended variant of
    the classic two-sample t-test).

        t = (mean(a) - mean(b)) / sqrt(var(a, ddof=1)/n_a + var(b, ddof=1)/n_b)
    """
    pass


def welch_degrees_of_freedom(a: np.ndarray, b: np.ndarray) -> float:
    """
    The Welch-Satterthwaite equation: the (generally non-integer)
    effective degrees of freedom for Welch's t-test, needed to look up
    the correct t-distribution for computing a p-value.

        df = (var_a/n_a + var_b/n_b)^2
             / ( (var_a/n_a)^2/(n_a-1) + (var_b/n_b)^2/(n_b-1) )
    """
    pass


def two_sample_t_test(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    """
    Returns (t_statistic, p_value) for a two-sided Welch's t-test
    comparing the means of `a` and `b`. Use welch_t_statistic and
    welch_degrees_of_freedom (both above) together with
    stats.t.cdf to compute the two-sided p-value:

        p = 2 * (1 - stats.t.cdf(|t|, df))
    """
    pass
