def latency_breakdown(events: list[tuple[str, float]]) -> dict[str, float]:
    breakdown: dict[str, float] = {}
    for component, duration in events:
        breakdown[component] = breakdown.get(component, 0.0) + duration
    return breakdown
