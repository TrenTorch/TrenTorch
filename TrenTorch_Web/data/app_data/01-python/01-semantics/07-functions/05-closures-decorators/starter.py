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


def add_call_count(function):
    """
    Return a wrapper around `function`.

    The wrapper must call the original function with the same
    positional and keyword arguments, return the original result,
    and maintain a call count that increases once per wrapper call,
    exposed as an attribute `.calls` on the returned wrapper.

    The count must belong to this particular decorated function
    and must not be shared by other decorated functions.

    Example:
        def add(a, b):
            return a + b

        wrapped = add_call_count(add)
        wrapped(2, 3) -> 5
        wrapped.calls -> 1
        wrapped(4, 5) -> 9
        wrapped.calls -> 2
    """
    pass


def run_with_message(function, message: str, *args, **kwargs):
    """
    Call `function` with `*args` and `**kwargs` and return its
    result.

    The function must be called exactly once.

    `message` is supplied separately and should not be passed to
    `function`.

    Example:
        run_with_message(pow, "running", 2, 3) -> 8
    """
    pass


def decorate_result(function, prefix: str):
    """
    Return a wrapper around a function that accepts one argument.

    The wrapper must call the original function with the supplied
    argument, convert the returned value to a string, prepend
    `prefix`, and return the resulting string.

    Example:
        def name(x): return x
        wrapped = decorate_result(name, "Name: ")
        wrapped("Ada") -> "Name: Ada"
    """
    pass
