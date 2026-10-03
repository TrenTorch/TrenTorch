def compute_remaining_steps(full_plan: list[str], completed_steps: list[str]) -> list[str] | str:
    if full_plan[: len(completed_steps)] != completed_steps:
        return "STATE_MISMATCH"
    return full_plan[len(completed_steps) :]
