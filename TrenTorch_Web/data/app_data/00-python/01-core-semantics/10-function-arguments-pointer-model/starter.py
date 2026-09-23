def append_in_place(lst: list, value) -> None:
    """
    Mutate `lst` directly by appending `value` to it. Do not
    return anything and do not reassign the `lst` parameter to
    a new object.
    """
    pass


def attempt_reassign(lst: list) -> None:
    """
    Inside this function, reassign the `lst` parameter to a
    brand-new list [0, 0, 0]. Do not mutate the original list
    the caller passed in. Return nothing.
    (This exists to demonstrate that the caller's list is
    unaffected by this reassignment.)
    """
    pass


def add_one(x: int) -> int:
    """
    Return x + 1. Since int is immutable, this cannot modify the
    caller's original integer — only a new int can be returned.
    """
    pass
