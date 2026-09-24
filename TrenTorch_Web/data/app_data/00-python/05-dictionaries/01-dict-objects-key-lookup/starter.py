def first_positions(words: list) -> dict:
    """
    Return a dictionary that maps each distinct word in `words`
    to the index of its FIRST occurrence. Later occurrences must
    not change the stored index. Use `in` to check for a key.

    Example: first_positions(["a", "b", "a"]) -> {"a": 0, "b": 1}
    """
    pass


def same_key(a, b) -> bool:
    """
    Return True if `a` and `b` would be treated as the same key
    by a dictionary: their hashes are equal AND they compare
    equal with ==. Both arguments are hashable.

    Example: same_key(1, 1.0) -> True
             same_key("a", "b") -> False
    """
    pass


def distinct_key_count(keys: list) -> int:
    """
    Create an empty dictionary, store every element of `keys` in
    it as a key (with any value), and return the number of
    entries in the dictionary afterward.

    Example: distinct_key_count([1, 1.0, True, "1"]) -> 2
    """
    pass
