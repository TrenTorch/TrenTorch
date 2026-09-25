def apply_once(function, value):
    """
    Call the supplied one-argument function with `value` and
    return its result.

    The function itself must be passed as an argument. Do not
    assume a particular function name or implementation.

    Example:
        apply_once(abs, -8) -> 8
    """
    pass


def apply_twice(function, value):
    """
    Call the supplied one-argument function twice in sequence.

    The result of the first call becomes the argument to the
    second call.

    Example:
        def add_one(x): return x + 1
        apply_twice(add_one, 5) -> 7
    """
    pass


def apply_n_times(function, value, count: int):
    """
    Apply the supplied one-argument function to `value` exactly
    `count` times and return the final result.

    If `count` is 0, return the original `value`.
    If `count` is negative, return the original `value`.

    Example:
        def double(x): return x * 2
        apply_n_times(double, 3, 3) -> 24
    """
    pass


def transform_all(values: list, function) -> list:
    """
    Return a new list containing the result of calling `function`
    once on every element of `values`, in input order.

    Do not modify `values`.

    Example:
        transform_all([1, -2, 3], abs) -> [1, 2, 3]
    """
    pass
