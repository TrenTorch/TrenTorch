def square(x):
    """
    Return the square of `x`.

    Example:
        square(5) -> 25
    """
    pass


def min_max(values):
    """
    Return a 2-element tuple `(minimum, maximum)` containing the
    smallest and largest values in `values`.

    `values` is a non-empty sequence. Do not use the built-in
    `min()` or `max()` functions.

    Example:
        min_max([4, 1, 7, 2]) -> (1, 7)
    """
    pass


def describe_pair(a, b):
    """
    Return a 3-element tuple:

        (sum, difference, product)

    where:
        - sum is `a + b`
        - difference is `a - b`
        - product is `a * b`

    Example:
        describe_pair(6, 2) -> (8, 4, 12)
    """
    pass


def absolute_value(x):
    """
    Return the absolute value of `x`.

    Do not use the built-in `abs()` function.

    Example:
        absolute_value(-7) -> 7
        absolute_value(4) -> 4
    """
    pass


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
