def replay_until_failure(steps: list[tuple[str, bool]]) -> list[str]:
    """Each step is (name, succeeded). Return the names of every step up to
    and including the first one where `succeeded` is False, then stop --
    steps after the first failure are never reached. If every step
    succeeds, return every step's name.
    """
    # TODO: implement
    pass
