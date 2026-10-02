def alias_and_call(function, value):
    """
    `function` is a function object that accepts one argument.
    Assign the function object to another local variable and call
    it with `value`. Return the function's result.

    Do not call `function` before assigning it to the local alias.

    Example:
        alias_and_call(lambda x: x * 2, 5) -> 10
    """
    pass


def apply_selected(functions: list, index: int, value):
    """
    `functions` is a non-empty list of one-argument function
    objects. Select the function at `index`, call it with `value`,
    and return its result.

    Negative indexes follow normal list indexing.

    Example:
        apply_selected([abs, str], 0, -7) -> 7
        apply_selected([abs, str], 1, 42) -> "42"
    """
    pass


def same_function(function_a, function_b) -> bool:
    """
    Return True only when `function_a` and `function_b` refer to
    the exact same function object. Use object identity rather
    than comparing the results of calling the functions.

    Example:
        def f(x): return x
        a = f
        same_function(f, a) -> True
    """
    pass


def apply_once(function, value):
    """
    Call the supplied one-argument function with `value` and
    return its result.

    The function itself must be passed as an argument. Do not
    assume a particular function name or implementation.

    Example:
        apply_once(abs, -8) -> 8
    """
    pass


def apply_twice(function, value):
    """
    Call the supplied one-argument function twice in sequence.

    The result of the first call becomes the argument to the
    second call.

    Example:
        def add_one(x): return x + 1
        apply_twice(add_one, 5) -> 7
    """
    pass


def apply_n_times(function, value, count: int):
    """
    Apply the supplied one-argument function to `value` exactly
    `count` times and return the final result.

    If `count` is 0, return the original `value`.
    If `count` is negative, return the original `value`.

    Example:
        def double(x): return x * 2
        apply_n_times(double, 3, 3) -> 24
    """
    pass


def transform_all(values: list, function) -> list:
    """
    Return a new list containing the result of calling `function`
    once on every element of `values`, in input order.

    Do not modify `values`.

    Example:
        transform_all([1, -2, 3], abs) -> [1, 2, 3]
    """
    pass


def make_square_function():
    """
    Return a lambda function that accepts one number and returns
    its square.

    Example:
        square = make_square_function()
        square(6) -> 36
    """
    pass


def make_offset_function(offset):
    """
    Return a lambda function that accepts one value and adds
    `offset` to it.

    The returned lambda must retain the `offset` supplied to
    this particular call.

    Example:
        add_five = make_offset_function(5)
        add_five(10) -> 15
    """
    pass


def apply_lambda(values: list, function) -> list:
    """
    Return a new list containing the result of calling the supplied
    function on every element of `values`, in order.

    The function may be a lambda or any other one-argument function.
    Do not modify `values`.

    Example:
        apply_lambda([1, 2, 3], lambda x: x * 2)
        -> [2, 4, 6]
    """
    pass
