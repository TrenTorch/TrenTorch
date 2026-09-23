def index_or_minus_one(lst: list, value) -> int:
    """
    Return the index of the first element of `lst` that matches
    `value`, or -1 if there is none. Do not let index() raise.
    """
    pass


def all_indices(lst: list, value) -> list:
    """
    Return a list of every index at which `lst` holds an element
    equal to `value`, in increasing order. Use enumerate().

    Example: all_indices([5, 3, 5, 7], 5) -> [0, 2]
    """
    pass


def contains_all(lst: list, needles: list) -> bool:
    """
    Return True if every element of `needles` is present in
    `lst`. An empty `needles` returns True.
    """
    pass


def contains_same_object(lst: list, target) -> bool:
    """
    Return True if some element of `lst` IS the exact object
    `target` (identity, using `is`), even if equal-looking
    objects elsewhere in the list do not count.

    Example: a = [1]; contains_same_object([[1], a], a) -> True
             contains_same_object([[1]], a)             -> False
    """
    pass
