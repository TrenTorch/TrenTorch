COUNTER = 0


def local_double(value):
    """
    Create a local variable containing `value * 2` and return it.

    The function must not create or modify a global variable named
    `result`.

    Example:
        local_double(5) -> 10
    """
    pass


def read_limit(value, limit):
    """
    Return True if `value` is less than or equal to the supplied
    `limit`, otherwise return False.

    Use the parameter `limit` as the local variable.

    Example:
        read_limit(5, 10) -> True
        read_limit(15, 10) -> False
    """
    pass


def increment_global():
    """
    A module-level integer variable named `COUNTER` is expected to
    exist.

    Use the `global` statement to increment `COUNTER` by 1 and
    return its new value.

    Example:
        if COUNTER == 4:
            increment_global() -> 5
    """
    pass


def mutate_shared(items, value):
    """
    Append `value` to the supplied list `items` and return the
    same list object.

    Do not create a replacement list.

    Example:
        xs = [1]
        result = mutate_shared(xs, 2)
        result == [1, 2]
        result is xs -> True
    """
    pass
