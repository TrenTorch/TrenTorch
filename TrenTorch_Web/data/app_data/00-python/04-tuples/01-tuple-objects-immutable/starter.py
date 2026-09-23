def make_singleton(x) -> tuple:
    """
    Return a tuple containing exactly one element: `x`.
    Example: make_singleton(5) -> (5,)
    """
    pass


def tuple_replace(t: tuple, index: int, value) -> tuple:
    """
    Return a NEW tuple equal to `t` with the element at
    position `index` replaced by `value`. `index` may be
    negative. If `index` is out of range, return `t` unchanged.
    Build the result with slicing and +; do not convert to a
    list.

    Example: tuple_replace((1, 2, 3), 1, 99) -> (1, 99, 3)
    """
    pass


def count_and_first_index(t: tuple, x) -> tuple:
    """
    Return a 2-element tuple (count, first_index) where `count`
    is how many elements of `t` equal `x`, and `first_index` is
    the position of the first such element, or -1 if there is
    none. Check `x in t` before calling index().

    Example: count_and_first_index((5, 3, 5), 5) -> (2, 0)
             count_and_first_index((5, 3, 5), 9) -> (0, -1)
    """
    pass
