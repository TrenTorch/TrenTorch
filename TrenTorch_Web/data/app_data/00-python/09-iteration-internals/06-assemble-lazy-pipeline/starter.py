def build_pipeline(source, transformations=(), predicates=()):
    """
    Build and return a LAZY iterator over `source`.

    `source` is any iterable.

    `transformations` is an iterable of one-argument functions.
    Each transformation must be applied in order.

    `predicates` is an iterable of one-argument functions.
    A value must pass every predicate to be yielded.

    For every source value:

        source value
            -> transformation 1
            -> transformation 2
            -> ...
            -> predicate 1
            -> predicate 2
            -> ...
            -> yield

    Requirements:

    1. Do not convert `source` into a list.
    2. Do not eagerly compute all transformed values.
    3. Produce values lazily using iteration/generator behavior.
    4. Preserve the order of values that pass.
    5. Apply transformations in the supplied order.
    6. Apply predicates after all transformations.
    7. If any predicate returns a falsy value, do not yield that
       value and continue processing later source values.
    8. Stop naturally when `source` is exhausted.
    9. Do not consume more source values than necessary when only
       a partial result is requested.

    Example:

        source = [1, 2, 3, 4, 5]

        transformations = [
            lambda x: x * 2
        ]

        predicates = [
            lambda x: x > 5
        ]

        list(build_pipeline(
            source,
            transformations,
            predicates
        ))

        -> [6, 8, 10]
    """
    pass
