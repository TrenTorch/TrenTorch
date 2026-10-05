import math


def nemenyi_cd(k: int, n: int, q_alpha: float) -> float:
    if k < 2:
        raise ValueError("need at least two algorithms")
    if n < 1:
        raise ValueError("need at least one dataset")
    if q_alpha <= 0:
        raise ValueError("q_alpha must be positive")
    return float(q_alpha * math.sqrt(k * (k + 1) / (6.0 * n)))


def significantly_different(rank_a: float, rank_b: float, cd: float) -> bool:
    if cd < 0:
        raise ValueError("cd must be nonnegative")
    return abs(rank_a - rank_b) >= cd
