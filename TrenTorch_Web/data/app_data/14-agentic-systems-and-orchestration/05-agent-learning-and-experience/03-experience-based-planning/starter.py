def pick_best_past_plan(query_task: str, past_plans: list[tuple[str, str, float]]) -> str | None:
    """
    query_task: the exact task name being planned for right now.
    past_plans: (task_name, plan, success_rate) for every past run
    logged, in order.

    Among entries whose task_name EXACTLY matches query_task, return
    the plan with the highest success_rate (ties broken by whichever
    was seen first in past_plans). Return None if no past plan exists
    for this exact task.
    """
    # TODO: Implement the exact-match-then-argmax lookup from Theory.
    pass
