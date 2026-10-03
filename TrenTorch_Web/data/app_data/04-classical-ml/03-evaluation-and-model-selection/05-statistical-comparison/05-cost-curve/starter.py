def normalized_expected_cost(
    fnr: float,
    fpr: float,
    pos_prior: float,
    cost_fn: float,
    cost_fp: float,
) -> float:
    """
    Drummond-Holte NEC = FNR * PC + FPR * (1 - PC), with
    PC = p C_FN / (p C_FN + (1 - p) C_FP). Raise ValueError for rates outside
    [0, 1], a prior outside (0, 1), or nonpositive costs.
    """
    pass
