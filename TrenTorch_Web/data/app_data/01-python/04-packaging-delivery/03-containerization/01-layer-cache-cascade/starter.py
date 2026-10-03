def rebuilt_steps(previous: list[tuple[str, str]], current: list[tuple[str, str]]) -> list[int]:
    """
    `previous` and `current` are the steps of the last build and of this
    build. Each step is an (instruction, input_digest) tuple.

    A step in `current` is served from cache only if it equals the step
    at the same index in `previous` AND every earlier step was also
    served from cache. Return the sorted indexes (into `current`) of the
    steps that must be rebuilt.
    """
    # TODO: implement this, see the Theory tab for the rules.
    pass
