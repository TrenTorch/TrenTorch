def lower_bound(a: list, x) -> int:
    """
    a: list sorted in non-decreasing order
    Returns the smallest index i such that every value before i is < x
    (len(a) if all values are smaller). O(log n); do not use bisect.
    """
    # TODO: Halve the interval until it is empty.
    pass


def upper_bound(a: list, x) -> int:
    """
    Returns the smallest index i such that every value before i is <= x
    (len(a) if all values are <= x). O(log n); do not use bisect.
    """
    # TODO: Like lower_bound, but equal values also count as too small.
    pass


def range_query(a: list, low, high) -> list:
    """
    Returns the values v of the sorted list with low <= v <= high, in
    order, using the two bounds above and one slice.
    """
    # TODO: Slice from lower_bound(low) to upper_bound(high).
    pass


def insert_sorted(a: list, x) -> list:
    """
    Returns a NEW sorted list with x inserted after any equal values.
    `a` must not be modified.
    """
    # TODO: Find the position with a bound, then build the new list.
    pass
