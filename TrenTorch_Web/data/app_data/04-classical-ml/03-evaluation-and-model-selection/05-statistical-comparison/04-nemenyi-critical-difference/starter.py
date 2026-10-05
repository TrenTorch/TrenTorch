import math


def nemenyi_cd(k: int, n: int, q_alpha: float) -> float:
    """
    Critical difference q_alpha * sqrt(k (k + 1) / (6 n)).
    Raise ValueError for k < 2, n < 1, or q_alpha <= 0.
    """
    pass


def significantly_different(rank_a: float, rank_b: float, cd: float) -> bool:
    """
    True when |rank_a - rank_b| >= cd. Raise ValueError for negative cd.
    """
    pass
