def sum_all(*values):
    """
    Return the sum of all positional arguments.

    If no arguments are supplied, return 0.

    Example:
        sum_all(1, 2, 3) -> 6
        sum_all() -> 0
    """
    pass


def collect_types(*values):
    """
    Return a tuple containing the type of every positional
    argument, in the same order.

    Example:
        collect_types(1, "x", 2.5)
        -> (int, str, float)
    """
    pass


def build_options(**options):
    """
    Return a NEW dictionary containing all supplied keyword
    arguments.

    Example:
        build_options(debug=True, retries=3)
        -> {"debug": True, "retries": 3}
    """
    pass


def summarize(required, *values, **options):
    """
    Return a dictionary with exactly three keys:

        "required" -> the value of `required`
        "values"   -> a tuple containing all extra positional values
        "options"  -> a dictionary containing all keyword arguments

    Do not modify any input objects.

    Example:
        summarize("x", 1, 2, debug=True)
        ->
        {
            "required": "x",
            "values": (1, 2),
            "options": {"debug": True}
        }
    """
    pass


def call_with_options(function, args, options):
    """
    Call `function` using `args` as positional arguments and
    `options` as keyword arguments.

    Return exactly whatever `function` returns.

    Example:
        call_with_options(pow, (2, 3), {}) -> 8

    `args` is a sequence and `options` is a dictionary.
    """
    pass
