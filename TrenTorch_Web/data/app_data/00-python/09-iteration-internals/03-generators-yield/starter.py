def generate_range(start: int, stop: int):
    """
    Yield integers starting at `start` and increasing by 1 until
    but not including `stop`.

    This must be a generator function using `yield`.

    Example:
        list(generate_range(2, 5)) -> [2, 3, 4]
        list(generate_range(5, 2)) -> []
    """
    pass


def generate_squares(values):
    """
    Lazily yield the square of every value produced by `values`,
    preserving iteration order.

    Do not build a list containing all squares before yielding.

    Example:
        list(generate_squares([1, 2, 3])) -> [1, 4, 9]
    """
    pass


def generate_until(values, limit):
    """
    Lazily yield values from `values` until the first value that
    is greater than `limit` is encountered.

    The value greater than `limit` must not be yielded, and no
    later values should be consumed.

    Example:
        list(generate_until([2, 4, 6, 8, 10], 6))
        -> [2, 4, 6]
    """
    pass
