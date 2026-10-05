def consume_iterator(iterable) -> list:
    """
    Obtain an iterator from `iterable` and manually consume it
    using `next()` until `StopIteration`.

    Return a new list containing all values in the original
    iteration order.

    Do not use a `for` loop.

    Example:
        consume_iterator([1, 2, 3]) -> [1, 2, 3]
        consume_iterator([]) -> []
    """
    pass


def take_first(iterable, count: int) -> list:
    """
    Obtain an iterator from `iterable` and consume at most
    `count` values using `next()`.

    If the iterable becomes exhausted before `count` values are
    produced, stop early.

    If `count <= 0`, return an empty list.

    Example:
        take_first([10, 20, 30], 2) -> [10, 20]
        take_first([10], 5) -> [10]
    """
    pass


def next_or_default(iterator, default):
    """
    Call `next()` on the supplied iterator.

    Return the next value if one exists. If the iterator is
    exhausted, return `default`.

    Do not treat a produced value such as None, 0, or False as
    exhaustion.
    """
    pass
