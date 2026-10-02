def is_iterator(obj) -> bool:
    """
    Return True if `obj` is an iterator.

    An iterator is an object for which `iter(obj)` returns the
    object itself.

    Example:
        values = [1, 2, 3]
        iterator = iter(values)

        is_iterator(values) -> False
        is_iterator(iterator) -> True
    """
    pass


def get_iterator(iterable):
    """
    Return an iterator obtained from `iterable`.

    Do not manually index into the iterable.

    Example:
        get_iterator([10, 20]) produces an iterator that yields
        10 and then 20.
    """
    pass


def independent_iterators(values: list) -> tuple:
    """
    Return two separate iterators created from `values`.

    Advancing one returned iterator must not advance the other.

    Example:
        a, b = independent_iterators([1, 2, 3])

        next(a) -> 1
        next(a) -> 2
        next(b) -> 1
    """
    pass
