def remove_all(lst: list, value) -> None:
    """
    Remove EVERY element equal to `value` from `lst`, in place
    (the caller's list object must keep its id()). Consecutive
    duplicates must all be removed. Return nothing.

    Example: lst = [1, 1, 2, 1]; remove_all(lst, 1)
             -> lst is now [2]
    """
    pass


def pop_last_n(lst: list, n: int) -> list:
    """
    Remove the last `n` elements of `lst` in place and return
    them in their ORIGINAL order as a new list. If n <= 0,
    remove nothing and return []. If n >= len(lst), remove
    everything.

    Example: lst = [1, 2, 3, 4]; pop_last_n(lst, 2) -> [3, 4]
             and lst is now [1, 2]
    """
    pass


def delete_every_other(lst: list) -> None:
    """
    Remove the elements at positions 0, 2, 4, ... from `lst`,
    in place, using del with an extended slice. Return nothing.

    Example: lst = [1, 2, 3, 4, 5] -> lst is now [2, 4]
    """
    pass


def remove_first_or_report(lst: list, value) -> bool:
    """
    If `value` is in `lst`, remove its first occurrence in place
    and return True. If it is not present, leave `lst` unchanged
    and return False. Check with `in` before removing; do not
    let remove() fail.
    """
    pass
