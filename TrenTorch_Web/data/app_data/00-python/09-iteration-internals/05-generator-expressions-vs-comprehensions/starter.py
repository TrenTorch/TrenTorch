def eager_double(values) -> list:
    """
    Return a concrete list containing every value in `values`
    multiplied by 2.

    The result must be fully materialized before the function
    returns.

    Example:
        eager_double([1, 2, 3]) -> [2, 4, 6]
    """
    pass


def lazy_double(values):
    """
    Return a generator expression that produces every value in
    `values` multiplied by 2.

    Do not construct the complete result list.

    Example:
        result = lazy_double([1, 2, 3])
        list(result) -> [2, 4, 6]
    """
    pass


def lazy_positive(values):
    """
    Return a generator expression that lazily produces only
    positive values from `values`.

    Do not eagerly construct a list.

    Example:
        list(lazy_positive([-2, 3, 0, 5])) -> [3, 5]
    """
    pass
