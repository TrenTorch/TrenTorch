def pick_model_under_budget(
    models: list[tuple[str, float, float]], latency_budget_ms: float
) -> str | None:
    """Each model is (name, quality_score, latency_ms). Among the models
    whose latency_ms is within latency_budget_ms, return the name of the
    one with the highest quality_score (first one wins on an exact tie).
    Return None if no model fits the budget.
    """
    # TODO: implement
    pass
