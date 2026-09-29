def safe_int(text, default: int) -> int:
    """
    Convert `text` to an int with int(). If the conversion
    raises a ValueError or a TypeError (for example when `text`
    is None), return `default` instead.
    Example: safe_int("42", 0) -> 42
             safe_int("x", -1) -> -1
             safe_int(None, -1) -> -1
    """
    pass


def parse_pair(text: str):
    """
    `text` should look like "a:b" with two integers separated by
    ":". Return a tuple (a, b) of the two integers. If `text`
    has no ":" or has more than one, or if either part is not a
    valid integer, return None. Use split(":") and int(), and
    handle the failures with try/except (do not pre-check with
    string methods for digits).
    Example: parse_pair("3:4") -> (3, 4)
    """
    pass


def run_steps(log: list, fail: bool) -> None:
    """
    Record which blocks run, in order, by appending strings to
    `log`. Write a try statement with try, except, else, and
    finally blocks:
      - try:     append "try"; then, if `fail` is True, raise a
                 ValueError("x")
      - except ValueError: append "except"
      - else:    append "else"
      - finally: append "finally"
    Return nothing. The ValueError must not escape the function.
    """
    pass


def count_convertible(items: list) -> int:
    """
    Return how many elements of `items` can be converted with
    int() without an error (ValueError or TypeError).
    Example: count_convertible(["1", "x", None, 3.9, "07"]) -> 3
    """
    pass


def cleanup_return(log: list, flag: bool) -> str:
    """
    Use a try/finally statement:
      - try: if `flag` is True, return the string "early"
             (otherwise do nothing and fall through)
      - finally: append "cleanup" to `log`
    If the function falls through the try block, return "end"
    after the try statement. Return "early" or "end" only; do
    not put a return inside the finally block.
    """
    pass
