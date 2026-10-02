def remove_keys(d: dict, keys: list) -> int:
    """
    Remove from `d`, in place, every key listed in `keys` that is
    present in `d`. Keys not present are ignored. `keys` may
    contain duplicates. Return the number of entries actually
    removed.

    Example: d = {"a": 1, "b": 2}; remove_keys(d, ["a", "z", "a"])
             -> returns 1, and d is now {"b": 2}
    """
    pass


def take_last(d: dict):
    """
    Remove the most recently inserted entry from `d`, in place,
    and return it as a (key, value) tuple. If `d` is empty,
    return None and leave `d` unchanged. Use popitem().
    """
    pass


def remove_and_return(d: dict, key, default):
    """
    Remove `key` from `d` in place and return its value. If the
    key is not present, return `default` and leave `d`
    unchanged. Use pop() with a default.
    """
    pass


def clear_and_report(d: dict) -> int:
    """
    Remove every entry from `d` in place and return how many
    entries there were before clearing.
    """
    pass
