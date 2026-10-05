def build_point(x, y):
    """
    Return a 2-element tuple `(x, y)`.

    The function must accept both positional and keyword calls.

    Example:
        build_point(3, 4) -> (3, 4)
        build_point(x=3, y=4) -> (3, 4)
    """
    pass


def configure_model(name, dimensions, metric):
    """
    Return a dictionary containing the supplied `name`,
    `dimensions`, and `metric`.

    The function should work correctly when the caller supplies
    the arguments positionally, by keyword, or using positional
    arguments followed by keyword arguments.

    Example:
        configure_model("db", 128, "cosine")
        -> {"name": "db", "dimensions": 128, "metric": "cosine"}
    """
    pass


def format_record(identifier, value, label):
    """
    Return a string in the exact form:

        "identifier=value [label]"

    The function must support positional and keyword arguments.

    Example:
        format_record(7, 3.5, "score")
        -> "7=3.5 [score]"
    """
    pass


def power(x, exponent=2):
    """
    Return `x` raised to `exponent`.

    If `exponent` is omitted, use 2.

    Example:
        power(5) -> 25
        power(2, 3) -> 8
    """
    pass


def make_label(value, prefix="item"):
    """
    Return a string in the form:

        "prefix:value"

    If `prefix` is omitted, use `"item"`.

    Example:
        make_label(7) -> "item:7"
        make_label(7, "id") -> "id:7"
    """
    pass


def append_value(value, items=None):
    """
    Return a list containing `value` appended to `items`.

    If `items` is omitted, create a NEW empty list for this call.

    If a list is supplied, mutate that supplied list by appending
    `value` and return the same list object.

    Example:
        append_value(1) -> [1]
        append_value(2) -> [2]

        xs = [10]
        result = append_value(20, xs)
        xs == [10, 20]
        result is xs -> True
    """
    pass


def describe_config(name, enabled=True, retries=3):
    """
    Return a tuple `(name, enabled, retries)`.

    `enabled` defaults to True and `retries` defaults to 3.

    Example:
        describe_config("server")
        -> ("server", True, 3)
    """
    pass


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
