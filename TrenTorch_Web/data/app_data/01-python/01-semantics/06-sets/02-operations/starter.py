def combine_sets(a: set, b: set) -> set:
    """
    Return the union of `a` and `b`.

    Neither input set may be modified.

    Example:
        combine_sets({1, 2}, {2, 3}) -> {1, 2, 3}
    """
    pass


def common_values(a: set, b: set) -> set:
    """
    Return the intersection of `a` and `b`.

    Neither input set may be modified.

    Example:
        common_values({1, 2, 3}, {2, 3, 4}) -> {2, 3}
    """
    pass


def only_in_first(a: set, b: set) -> set:
    """
    Return the elements that occur in `a` but not in `b`.

    Neither input set may be modified.

    Example:
        only_in_first({1, 2, 3}, {2, 4}) -> {1, 3}
    """
    pass


def in_exactly_one(a: set, b: set) -> set:
    """
    Return the symmetric difference of `a` and `b`.

    The result contains elements that occur in exactly one of
    the two sets.

    Example:
        in_exactly_one({1, 2, 3}, {2, 3, 4}) -> {1, 4}
    """
    pass


def relationship(a: set, b: set) -> tuple:
    """
    Return a 3-element tuple:

        (is_subset, is_superset, is_disjoint)

    where:
        - is_subset is True when `a` is a subset of `b`
        - is_superset is True when `a` is a superset of `b`
        - is_disjoint is True when `a` and `b` have no elements
          in common

    Example:
        relationship({1, 2}, {1, 2, 3})
        -> (True, False, False)
    """
    pass
