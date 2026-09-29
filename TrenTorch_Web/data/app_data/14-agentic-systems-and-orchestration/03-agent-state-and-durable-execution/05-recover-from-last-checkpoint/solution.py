def find_recovery_checkpoint(checkpoints: list[tuple[int, dict]], crash_step: int) -> dict | None:
    best_snapshot: dict | None = None
    best_step = -1
    for step, snapshot in checkpoints:
        if step <= crash_step and step > best_step:
            best_snapshot = snapshot
            best_step = step
    return best_snapshot
