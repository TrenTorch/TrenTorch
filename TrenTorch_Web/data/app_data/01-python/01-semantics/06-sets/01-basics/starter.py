def unique_values(values) -> set:
    """
    Return a set containing each distinct element from `values`.

    `values` may be any iterable whose elements are hashable.
    Duplicate elements must appear only once in the returned set.

    Example:
        unique_values([1, 2, 2, 3, 1]) -> {1, 2, 3}
    """
    pass


def contains_all(values, candidates) -> bool:
    """
    Return True if every element in `candidates` is present in
    `values`, and False otherwise.

    Convert `values` to a set so membership can be tested using
    set membership.

    Example:
        contains_all([1, 2, 3, 4], [2, 4]) -> True
        contains_all([1, 2, 3], [2, 5]) -> False
    """
    pass


def unique_count(values) -> int:
    """
    Return the number of distinct elements in `values`.

    Example:
        unique_count([1, 2, 2, 3, 3, 3]) -> 3
    """
    pass


def add_values(values, additions) -> set:
    """
    Create a set from `values`, add every element from `additions`,
    and return the resulting set.

    The original `values` object must not be modified.

    Example:
        add_values({1, 2}, [2, 3, 4]) -> {1, 2, 3, 4}
    """
    pass


def remove_if_present(values: set, value) -> set:
    """
    Return the same set object after removing `value` if it is
    present.

    Use `discard`, not `remove`, so an absent value does not
    raise an exception.

    Example:
        s = {1, 2, 3}
        result = remove_if_present(s, 2)
        s -> {1, 3}
        result is s -> True
    """
    pass


def remove_required(values: set, value) -> set:
    """
    Remove `value` from `values` using `remove` and return the
    same set object.

    If `value` is absent, allow the resulting `KeyError` to occur.

    Example:
        s = {1, 2, 3}
        remove_required(s, 2) -> {1, 3}
    """
    pass


def empty_set(values: set) -> set:
    """
    Remove every element from `values` using `clear` and return
    the same set object.

    Example:
        s = {1, 2, 3}
        result = empty_set(s)
        result == set()
        result is s -> True
    """
    pass
