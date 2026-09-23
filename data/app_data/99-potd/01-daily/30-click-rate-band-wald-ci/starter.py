import math

Z_95 = 1.959964


def click_rate_band(n: int, clicks: int) -> tuple[float, float, float]:
    """
    Wald 95% confidence interval for a click-through rate.

    n: sample size. clicks: number of successes, 0 <= clicks <= n.

    p_hat = clicks / n
    SE = sqrt(p_hat * (1 - p_hat) / n)
    Return (p_hat, p_hat - Z_95*SE, p_hat + Z_95*SE), using the fixed
    Z_95 = 1.959964 (not a runtime inverse-CDF call).

    clicks == 0 or clicks == n makes SE == 0, collapsing the interval to a
    single point, a known Wald-interval property, not a bug to correct.
    """
    # TODO: compute SE from p_hat itself, so both collapse cases fall out for free.
    pass
