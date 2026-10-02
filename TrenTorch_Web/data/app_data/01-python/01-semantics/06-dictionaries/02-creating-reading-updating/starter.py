def word_frequencies(text: str) -> dict:
    """
    Split `text` on whitespace and return a dictionary mapping
    each word to the number of times it occurs. Case matters:
    "The" and "the" are different words. Use get() with a
    default of 0.

    Example: word_frequencies("a b a") -> {"a": 2, "b": 1}
    """
    pass


def safe_lookup(d: dict, key, default):
    """
    Return the value stored under `key` in `d`, or `default` if
    `key` is not present. Do not modify `d`. Use get().
    """
    pass


def increment(d: dict, key, amount: int) -> None:
    """
    Add `amount` to the number stored under `key` in `d`, in
    place. If `key` is not present, store `amount` under it.
    Return nothing.
    """
    pass


def dict_from_two_lists(keys: list, values: list) -> dict:
    """
    `keys` and `values` are lists of the same length. Return a
    new dictionary that maps keys[i] to values[i] for every
    position i. Use an index loop (range and len). If a key
    repeats, the LAST value wins.

    Example: dict_from_two_lists(["a", "b"], [1, 2]) -> {"a": 1, "b": 2}
    """
    pass
