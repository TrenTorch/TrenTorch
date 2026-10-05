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


def freeze_rows(matrix: list) -> tuple:
    """
    `matrix` is a list of lists. Return a tuple of tuples with
    the same elements: each row becomes a tuple, and the outer
    list becomes a tuple. `matrix` must not be modified.

    Example: freeze_rows([[1, 2], [3]]) -> ((1, 2), (3,))
    """
    pass


def thaw_rows(frozen: tuple) -> list:
    """
    `frozen` is a tuple of tuples. Return a list of lists with
    the same elements. The result's rows must be new list
    objects that can be mutated without affecting anything else.

    Example: thaw_rows(((1, 2), (3,))) -> [[1, 2], [3]]
    """
    pass


def updated(seq, index: int, value):
    """
    `seq` is either a list or a tuple. Return a NEW sequence of
    the SAME type as `seq` in which the element at `index` is
    replaced by `value`. `seq` must never be modified. If
    `index` is out of range, return a new sequence of the same
    type with unchanged contents.
    Use isinstance() to decide the type.

    Example: updated([1, 2, 3], 0, 9) -> [9, 2, 3]
             updated((1, 2, 3), 0, 9) -> (9, 2, 3)
    """
    pass


def has_mutable_element(t: tuple) -> bool:
    """
    Return True if any element of the tuple `t` is a list, a
    dict, or a set (a mutable object whose contents could still
    change even though the tuple cannot). Otherwise return
    False. Check only the direct elements of `t`.
    Use isinstance().

    Example: has_mutable_element((1, [2])) -> True
             has_mutable_element((1, (2,))) -> False
    """
    pass
