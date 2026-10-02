def find_recovery_checkpoint(checkpoints: list[tuple[int, dict]], crash_step: int) -> dict | None:
    """
    checkpoints: (step_number, state_snapshot) pairs saved over the
    course of a run, not necessarily in step order.
    crash_step: the step number the run was on when it crashed.

    Return the state_snapshot of the checkpoint with the LARGEST
    step_number that is still <= crash_step -- the most recent valid
    recovery point at or before the crash. Return None if no
    checkpoint qualifies (every saved checkpoint is after crash_step).
    """
    # TODO: Implement the latest-valid-checkpoint search from Theory.
    pass
