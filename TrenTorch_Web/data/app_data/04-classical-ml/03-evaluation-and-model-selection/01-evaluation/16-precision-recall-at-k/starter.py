def precision_at_k(ranked: list, relevant, k: int) -> float:
    """
    ranked: item ids, best first.
    relevant: collection of relevant item ids.

    Returns:
        fraction of the top k slots that hold relevant items (0.0 if k <= 0).
    """
    # TODO: Count hits in ranked[:k] and divide by k.
    pass


def recall_at_k(ranked: list, relevant, k: int) -> float:
    """
    Returns:
        fraction of all relevant items found in the top k
        (0.0 if there are no relevant items or k <= 0).
    """
    # TODO: Same hit count, different denominator.
    pass
