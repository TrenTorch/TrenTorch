import math


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
