def compute_remaining_steps(full_plan: list[str], completed_steps: list[str]) -> list[str] | str:
    """
    full_plan: the run's full, fixed plan (the current, resumed
    session's view of it).
    completed_steps: the steps the saved (paused) session recorded as
    already done, in order.

    Resuming is only safe if completed_steps is exactly a PREFIX of
    full_plan -- i.e. the plan hasn't changed underneath the paused
    run. If it is, return the remaining steps (everything after the
    completed prefix). If completed_steps diverges from full_plan
    anywhere, the saved state no longer matches the current plan --
    return the literal string "STATE_MISMATCH" instead of guessing.
    """
    # TODO: Implement the prefix-validate-then-continue logic from Theory.
    pass
