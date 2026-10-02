def make_pipeline(*transformations):
    """
    Return a callable pipeline that applies every supplied
    one-argument function to its input in the exact order given.

    Example:
        pipeline = make_pipeline(
            lambda x: x + 2,
            lambda x: x * 3,
        )

        pipeline(4) -> 18

    The returned pipeline must:

    1. Accept exactly one input value.
    2. Apply each transformation to the current value in order.
    3. Return the final value.
    4. Return the original input unchanged when no transformations
       are supplied.
    5. Retain its own transformation configuration using the
       enclosing scope.
    6. Keep separate configurations independent when
       `make_pipeline` is called multiple times.
    7. Be wrapped with a decorator that counts how many times the
       returned pipeline has been called, exposed as `.calls`.
    8. Keep the call-count state private to that particular
       returned pipeline.
    9. Return the actual transformation result unchanged.

    The implementation may use *args, a nested function, a
    closure, lambda functions in tests, and a decorator.
    """
    pass
