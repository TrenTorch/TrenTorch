def squared(values):
    """
    Return a lazy map object that applies a square operation to
    every value in `values`.

    Example:
        list(squared([1, 2, 3])) -> [1, 4, 9]
    """
    pass


def keep_positive(values):
    """
    Return a lazy filter object containing only values greater
    than zero.

    Example:
        list(keep_positive([-2, 0, 3, 5])) -> [3, 5]
    """
    pass


def transform_and_filter(values, transform, predicate):
    """
    Return a lazy pipeline that first applies `transform` to each
    value and then keeps only transformed values for which
    `predicate` returns a truthy value.

    Do not eagerly construct a list.

    Example:
        transform_and_filter(
            [1, 2, 3],
            lambda x: x * 2,
            lambda x: x > 2
        )

        -> lazily produces 4 and 6
    """
    pass
