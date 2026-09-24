def percentage(value: float, total: float) -> float:
    """
    Return `value / total * 100`.

    `total` must not be zero.

    Example:
        percentage(25, 200) -> 12.5
    """
    pass


def repeat_text(text: str, count: int) -> str:
    """
    Return `text` repeated `count` times.

    `count` is expected to be non-negative.

    Example:
        repeat_text("ab", 3) -> "ababab"
    """
    pass


def make_pair(first, second) -> tuple:
    """
    Return a 2-element tuple `(first, second)`.

    The two values are returned in the same order they were
    supplied.

    Example:
        make_pair(1, "x") -> (1, "x")
    """
    pass


def function_metadata():
    """
    Return a dictionary containing metadata about this function.

    The returned dictionary must have exactly two keys:

        "doc" -> this function's docstring
        "annotations" -> this function's annotations dictionary

    The function must obtain both values from the function object
    itself rather than hard-coding them.
    """
    pass
