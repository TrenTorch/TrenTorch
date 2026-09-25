def make_multiplier(factor):
    """
    Return a new one-argument function that multiplies its input
    by `factor`.

    The returned function must retain access to the `factor`
    belonging to this particular call to `make_multiplier`.

    Example:
        double = make_multiplier(2)
        double(7) -> 14
    """
    pass


def make_prefixer(prefix: str):
    """
    Return a function that accepts one string and returns that
    string with `prefix` placed before it.

    The returned function must use the `prefix` from this
    particular call.

    Example:
        error = make_prefixer("ERROR: ")
        error("disk full") -> "ERROR: disk full"
    """
    pass


def make_counter(start: int):
    """
    Return a zero-argument function that maintains a private
    counter starting at `start`.

    Each call to the returned function increments the counter
    by 1 and returns the new value.

    Separate calls to `make_counter` must create independent
    counters.

    Example:
        counter = make_counter(10)
        counter() -> 11
        counter() -> 12
    """
    pass
