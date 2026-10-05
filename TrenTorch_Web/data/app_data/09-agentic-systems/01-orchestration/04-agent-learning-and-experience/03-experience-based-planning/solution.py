def pick_best_past_plan(query_task: str, past_plans: list[tuple[str, str, float]]) -> str | None:
    best_plan: str | None = None
    best_rate = -1.0
    for task_name, plan, success_rate in past_plans:
        if task_name == query_task and success_rate > best_rate:
            best_plan = plan
            best_rate = success_rate
    return best_plan
