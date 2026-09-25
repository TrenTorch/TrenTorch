def sum_of_values(d: dict) -> int:
    """
    `d` maps keys to numbers. Return the sum of all values. An
    empty dictionary returns 0. Use values().
    """
    pass


def keys_with_max_value(d: dict) -> list:
    """
    `d` maps keys to numbers. Return a list of every key whose
    value equals the maximum value, in the dictionary's
    insertion order. An empty dictionary returns [].

    Example: keys_with_max_value({"a": 3, "b": 5, "c": 5})
             -> ["b", "c"]
    """
    pass


def remove_where_value_below(d: dict, threshold: int) -> None:
    """
    Remove, in place, every entry of `d` whose value is less than
    `threshold`. Do not trigger a "changed size during
    iteration" error. Return nothing.
    """
    pass


def value_of(pair: tuple):
    """
    Return the second element of a (key, value) pair.
    """
    pass


def items_by_value_desc(d: dict) -> list:
    """
    Return a list of (key, value) tuples ordered by value from
    largest to smallest. Entries with equal values must appear in
    ascending key order. Use two stable sorts: first
    sorted(d.items()), then sorted(..., key=value_of,
    reverse=True). `d` must not be modified.
    """
    pass
