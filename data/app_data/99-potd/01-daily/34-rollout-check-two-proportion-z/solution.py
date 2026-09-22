import math


def _standard_normal_cdf(t: float) -> float:
    return 0.5 * (1.0 + math.erf(t / math.sqrt(2.0)))


def two_proportion_z_test(n1: int, x1: int, n2: int, x2: int) -> tuple[float, float, float, float]:
    p1 = x1 / n1
    p2 = x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)

    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = 0.0 if se == 0.0 else (p2 - p1) / se

    pvalue = 2 * (1 - _standard_normal_cdf(abs(z)))
    return p1, p2, z, pvalue
