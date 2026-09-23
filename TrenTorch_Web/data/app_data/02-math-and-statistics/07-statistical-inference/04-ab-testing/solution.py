import math

import numpy as np


def conversion_rate(conversions: int, visitors: int) -> float:
    return conversions / visitors


def two_proportion_z_test(
    conversions_a: int, visitors_a: int, conversions_b: int, visitors_b: int
) -> tuple[float, float]:
    p_a = conversion_rate(conversions_a, visitors_a)
    p_b = conversion_rate(conversions_b, visitors_b)
    p_pooled = (conversions_a + conversions_b) / (visitors_a + visitors_b)

    standard_error = np.sqrt(p_pooled * (1.0 - p_pooled) * (1.0 / visitors_a + 1.0 / visitors_b))
    z_statistic = (p_a - p_b) / standard_error
    standard_normal_cdf = 0.5 * (1.0 + math.erf(abs(z_statistic) / math.sqrt(2.0)))
    p_value = 2.0 * (1.0 - standard_normal_cdf)
    return float(z_statistic), float(p_value)
