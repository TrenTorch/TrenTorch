def merge_prefer_second(a: dict, b: dict) -> dict:
    """
    Return a NEW dictionary containing every entry of `a` and
    every entry of `b`. If a key is in both, the value from `b`
    is used. Neither `a` nor `b` may be modified. Build the
    result by copying `a` with dict(a) and then calling update().
    """
    pass


def merge_counts(a: dict, b: dict) -> dict:
    """
    `a` and `b` map keys to integer counts. Return a NEW
    dictionary in which each key's value is the sum of its
    values in `a` and `b` (a missing key counts as 0). Neither
    input may be modified.

    Example: merge_counts({"x": 1, "y": 2}, {"y": 3, "z": 4})
             -> {"x": 1, "y": 5, "z": 4}
    """
    pass


def group_by_first_letter(words: list) -> dict:
    """
    Return a dictionary that maps each first letter (lowercase)
    to a list of the words that start with it, in input order.
    Use setdefault() to create each list. Ignore empty strings.
    Matching is case-insensitive for the key, but the words are
    stored as given.

    Example: group_by_first_letter(["Apple", "avocado", "Bean"])
             -> {"a": ["Apple", "avocado"], "b": ["Bean"]}
    """
    pass


def add_defaults(config: dict, defaults: dict) -> None:
    """
    Add to `config`, in place, every entry of `defaults` whose
    key is not already in `config`. Existing keys keep their
    values. Use setdefault(). Return nothing.
    """
    pass
