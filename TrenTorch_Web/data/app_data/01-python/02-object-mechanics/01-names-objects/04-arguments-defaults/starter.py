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
    caller's original integer, only a new int can be returned.
    """
    pass


def add_item_fixed(item, bucket: list | None = None) -> list:
    """
    Append `item` to `bucket` and return it. If `bucket` is not
    provided (None), create a brand-new empty list inside this
    call, never reuse a list object across separate calls that
    didn't explicitly pass one.
    """
    pass


def is_vulnerable_to_mutable_default(func) -> bool:
    """
    Given a function object `func`, inspect its default argument
    values (available via func.__defaults__) and return True if
    any default value is a mutable object (list, dict, or set),
    False otherwise.
    """
    pass
