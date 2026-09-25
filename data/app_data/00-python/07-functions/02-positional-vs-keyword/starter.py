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
