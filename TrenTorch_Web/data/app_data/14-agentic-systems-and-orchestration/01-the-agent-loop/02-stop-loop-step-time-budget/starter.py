def find_loop_stop(
    steps: list[tuple[float, str]], max_steps: int, max_seconds: float
) -> tuple[int, str]:
    """
    steps: (elapsed_seconds_after_this_step, action) for every step
    actually taken, in order. elapsed_seconds is cumulative from the
    run's start.

    Walk the steps in order (1-indexed). At each step, check in this
    priority order and return the FIRST that applies:
      1. action == "finish"          -> (step_number, "FINISHED")
      2. step_number >= max_steps    -> (step_number, "STEP_BUDGET")
      3. elapsed_seconds >= max_seconds -> (step_number, "TIME_BUDGET")

    Returns (stop_step, reason) for whichever condition trips first.
    """
    # TODO: Implement the priority check from Theory.
    pass
