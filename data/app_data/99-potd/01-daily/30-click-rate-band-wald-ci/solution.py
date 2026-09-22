import math

Z_95 = 1.959964


def click_rate_band(n: int, clicks: int) -> tuple[float, float, float]:
    p_hat = clicks / n
    se = math.sqrt(p_hat * (1 - p_hat) / n)
    return p_hat, p_hat - Z_95 * se, p_hat + Z_95 * se
