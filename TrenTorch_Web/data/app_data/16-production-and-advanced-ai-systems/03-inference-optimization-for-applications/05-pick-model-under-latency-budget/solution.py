def pick_model_under_budget(
    models: list[tuple[str, float, float]], latency_budget_ms: float
) -> str | None:
    best_name = None
    best_quality = None
    for name, quality_score, latency_ms in models:
        if latency_ms <= latency_budget_ms:
            if best_quality is None or quality_score > best_quality:
                best_name = name
                best_quality = quality_score
    return best_name
