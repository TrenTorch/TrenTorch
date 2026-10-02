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
