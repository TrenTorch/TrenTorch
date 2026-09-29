def append_all(lst: list, items: list) -> None:
    """
    Add every element of `items` to the end of `lst`, in place,
    so that each element becomes its own new element of `lst`.
    Use extend(). Return nothing.
    """
    pass


def insert_sorted(lst: list, value) -> None:
    """
    `lst` is sorted in ascending order. Insert `value` in place
    so that the list stays sorted, placing it AFTER any existing
    elements equal to `value`. Use a loop to find the position
    and insert() to add it. Return nothing.

    Example: lst = [1, 3, 3, 5]; insert_sorted(lst, 3)
             -> lst is now [1, 3, 3, 3, 5]
    """
    pass


def flatten_one_level(list_of_lists: list) -> list:
    """
    Return a NEW list made of the elements of each inner list,
    in order. Do not change `list_of_lists` or its inner lists.
    Use extend() on a fresh list.

    Example: flatten_one_level([[1, 2], [], [3]]) -> [1, 2, 3]
    """
    pass


def concat_identity_report(lst: list, extra: list) -> list:
    """
    Using the list `lst` given by the caller:
      1. Record id(lst). Perform `lst += extra`. Record whether
         id(lst) is unchanged (call this same_after_iadd).
      2. Record id(lst) again. Perform `lst = lst + extra`.
         Record whether id(lst) is unchanged (same_after_plus).
    Return a list [same_after_iadd, same_after_plus].
    (The caller's original list is changed by step 1 only.)
    """
    pass
