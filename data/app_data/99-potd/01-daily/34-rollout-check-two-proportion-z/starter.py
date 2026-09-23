import math


def _standard_normal_cdf(t: float) -> float:
    return 0.5 * (1.0 + math.erf(t / math.sqrt(2.0)))


def two_proportion_z_test(n1: int, x1: int, n2: int, x2: int) -> tuple[float, float, float, float]:
    """
    Two-proportion z-test (control = group 1, treatment = group 2).

    n1, x1: control sample size and successes. n2, x2: treatment's.

    p1 = x1/n1, p2 = x2/n2, p_pool = (x1+x2)/(n1+n2)
    SE = sqrt(p_pool * (1-p_pool) * (1/n1 + 1/n2))
    z = (p2 - p1) / SE

    Return (p1, p2, z, pvalue), pvalue the two-sided p-value from the
    standard normal CDF. If SE is exactly 0 (e.g. x1 == x2 == 0), set
    z = 0.0 directly instead of dividing.
    """
    # TODO: p_pool is the POOLED rate across both groups, not (p1+p2)/2.
    pass
