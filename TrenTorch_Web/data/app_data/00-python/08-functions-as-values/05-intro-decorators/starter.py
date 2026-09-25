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
