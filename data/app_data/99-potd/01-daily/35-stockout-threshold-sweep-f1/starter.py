def best_f1_threshold(scores: list[float], y: list[int]) -> tuple[float, float]:
    """
    The score threshold that maximizes F1 (predict positive if score >= t).

    scores: n predicted scores. y: n true labels, each 0 or 1.

    For each distinct value in scores, using it as threshold t, compute
    F1(t) over the whole dataset. Return (best_threshold, best_f1).

    Ties for the best F1 are broken by the LARGER threshold. A threshold
    where precision or recall is undefined (a zero denominator) can never
    win. Sort once and sweep with running TP/FP counts, O(n log n), not
    a from-scratch recompute per threshold.
    """
    # TODO: sort by score descending, group equal scores together (they
    # share one threshold), and only update the best on a STRICT improvement.
    pass
