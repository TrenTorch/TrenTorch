def run_pipeline(values: list, *transformations, **options) -> list:
    """
    Apply a sequence of transformation functions to every value
    in `values` and return the resulting values as a new list.

    Each transformation must accept one value and return one value.
    Transformations are applied in the order supplied.

    Supported keyword options:

        unique
            Boolean. If True, include each final output value only
            once, preserving the order of its first occurrence.
            Defaults to False.

        limit
            Integer or None. If an integer is supplied, stop after
            collecting at most `limit` output values. Defaults to
            None, meaning no limit. `limit` must not be negative.

    Unknown keyword options must raise `TypeError`.

    If `unique=True`, use a set to track values already emitted
    and a list to preserve the output order.

    If `limit == 0`, return an empty list.

    The input `values` must not be modified.

    Example:

        def double(x):
            return x * 2

        def increment(x):
            return x + 1

        run_pipeline([1, 2, 3], double, increment)
        -> [3, 5, 7]

        run_pipeline(
            [1, 1, 2, 2],
            unique=True
        )
        -> [1, 2]
    """
    pass
