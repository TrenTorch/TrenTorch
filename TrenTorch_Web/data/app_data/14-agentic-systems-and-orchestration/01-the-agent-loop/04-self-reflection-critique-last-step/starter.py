def find_abandon_point(
    observations: list[str], failure_keywords: list[str], max_consecutive_failures: int
) -> int | None:
    """
    observations: each step's observation text, in order.
    failure_keywords: substrings (case-sensitive) that indicate this
    observation looks like a failure.
    max_consecutive_failures: how many failures in a row before the
    agent should give up.

    An observation "looks like a failure" if it contains ANY of
    failure_keywords as a substring. Track a running count of
    CONSECUTIVE failure-looking observations (any success resets the
    count to zero). Return the 1-indexed step at which that running
    count first reaches max_consecutive_failures, or None if it never
    does.
    """
    # TODO: Implement the consecutive-failure tracker from Theory.
    pass
