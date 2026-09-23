def find_loop_stop(
    steps: list[tuple[float, str]], max_steps: int, max_seconds: float
) -> tuple[int, str]:
    for i, (elapsed_seconds, action) in enumerate(steps, start=1):
        if action == "finish":
            return i, "FINISHED"
        if i >= max_steps:
            return i, "STEP_BUDGET"
        if elapsed_seconds >= max_seconds:
            return i, "TIME_BUDGET"
    return len(steps), "STEP_BUDGET"
