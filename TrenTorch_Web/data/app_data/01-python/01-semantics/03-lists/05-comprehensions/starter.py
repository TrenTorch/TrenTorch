import math


def squares_of_evens(numbers: list) -> list:
    """
    Return a new list of n * n for every even n in `numbers`,
    in order. Use a list comprehension with a filter.
    Example: squares_of_evens([1, 2, 3, 4]) -> [4, 16]
    """
    pass


def label_parity(numbers: list) -> list:
    """
    Return a new list the same length as `numbers` in which each
    element is "even" or "odd" according to the matching input
    number. Use a conditional expression in the comprehension.
    Example: label_parity([1, 2]) -> ["odd", "even"]
    """
    pass


def flatten(nested: list) -> list:
    """
    `nested` is a list of lists. Return a single new list with
    all inner elements in order. Use one comprehension with two
    for clauses.
    Example: flatten([[1, 2], [], [3]]) -> [1, 2, 3]
    """
    pass


def multiplication_table(n: int) -> list:
    """
    Return an n-by-n list of lists in which the entry at row
    i and column j (both starting at 1) is i * j. Use a nested
    comprehension. If n <= 0, return [].
    Example: multiplication_table(2) -> [[1, 2], [2, 4]]
    """
    pass


def elementwise(func, *vectors) -> list:
    """
    Apply `func` position by position across one or more lists.
    Return a NEW list whose element i is
        func(vectors[0][i], vectors[1][i], ...)
    Stop at the end of the SHORTEST input (use zip with argument
    unpacking). With no vectors, return [].

    Example: elementwise(lambda a, b: a + b, [1, 2], [10, 20]) -> [11, 22]
    """
    pass


def mask_select(values: list, mask: list) -> list:
    """
    Return a NEW list of the elements of `values` whose matching
    element in `mask` is truthy. Pair them with zip (so the
    shorter of the two decides the length).

    Example: mask_select([5, 6, 7], [True, False, True]) -> [5, 7]
    """
    pass


def broadcast_add(values: list, other) -> list:
    """
    Return a NEW list. If `other` has a length (hasattr
    "__len__"), add it element-wise to `values` (stop at the
    shorter length). Otherwise treat `other` as a single number
    and add it to every element of `values`.

    Example: broadcast_add([1, 2, 3], 10)       -> [11, 12, 13]
             broadcast_add([1, 2, 3], [1, 1, 1]) -> [2, 3, 4]
    """
    pass


def normalize(values: list, eps: float) -> list:
    """
    Layer-normalize `values`:
        mean      = sum(values) / n
        variance  = sum((x - mean) ** 2 for x in values) / n
        result[i] = (values[i] - mean) / sqrt(variance + eps)
    Return a NEW list. An empty `values` returns []. Use
    comprehensions and math.sqrt; the input must not be modified.
    """
    pass
