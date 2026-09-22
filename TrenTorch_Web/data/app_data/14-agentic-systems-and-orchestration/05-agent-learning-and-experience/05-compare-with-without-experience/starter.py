def compare_experience_impact(
    with_experience: list[bool], without_experience: list[bool]
) -> dict:
    """
    with_experience: per-task success (True/False) for the agent WITH
    access to past experience.
    without_experience: per-task success for the same tasks, in the
    same order, WITHOUT access to past experience.

    Compute:
      "with_success_rate": fraction of tasks the with-experience agent
          succeeded on
      "without_success_rate": same, for the without-experience agent
      "tasks_only_with_helped": count of tasks where the with-
          experience agent succeeded AND the without-experience agent
          failed on that same task
      "delta": with_success_rate - without_success_rate

    Both lists are the same length (same tasks, same order).

    Returns the dict with exactly these four keys.
    """
    # TODO: Implement the comparison stats from Theory.
    pass
