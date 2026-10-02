def square_map(n: int) -> dict:
    """
    Return a dictionary mapping each integer i from 1 to n
    (inclusive) to i * i. If n < 1, return {}.
    Use a dictionary comprehension.

    Example: square_map(3) -> {1: 1, 2: 4, 3: 9}
    """
    pass


def invert(d: dict) -> dict:
    """
    Return a NEW dictionary that maps each value of `d` to its
    key. If several keys share a value, the key that appears
    LATER in `d` is kept. Use a comprehension over items().
    `d` must not be modified.

    Example: invert({"a": 1, "b": 2}) -> {1: "a", 2: "b"}
    """
    pass


def filter_items(d: dict, min_value: int) -> dict:
    """
    Return a NEW dictionary containing only the entries of `d`
    whose value is >= `min_value`, in the original order.
    Use a comprehension.
    """
    pass


def dict_from_parallel(keys: list, values: list) -> dict:
    """
    Return a dictionary pairing keys[i] with values[i]. If the
    lists have different lengths, use only the first
    min(len(keys), len(values)) pairs. Use a comprehension with
    zip().
    """
    pass
