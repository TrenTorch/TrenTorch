def normalized_expected_cost(
    fnr: float,
    fpr: float,
    pos_prior: float,
    cost_fn: float,
    cost_fp: float,
) -> float:
    if not (0.0 <= fnr <= 1.0) or not (0.0 <= fpr <= 1.0):
        raise ValueError("error rates must lie in [0, 1]")
    if not (0.0 < pos_prior < 1.0):
        raise ValueError("pos_prior must lie in (0, 1)")
    if cost_fn <= 0 or cost_fp <= 0:
        raise ValueError("costs must be strictly positive")
    pc = pos_prior * cost_fn / (pos_prior * cost_fn + (1.0 - pos_prior) * cost_fp)
    return float(fnr * pc + fpr * (1.0 - pc))
