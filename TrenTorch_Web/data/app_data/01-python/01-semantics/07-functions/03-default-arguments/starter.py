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
