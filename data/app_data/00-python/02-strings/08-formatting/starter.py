def receipt_line(item: str, qty: int, price: float) -> str:
    """
    Return one line with these three fields concatenated:
      - `item` left-aligned in a field of width 12
      - `qty` right-aligned in a field of width 4
      - `price` right-aligned in a field of width 10, with
        exactly 2 decimal places
    Use an f-string.

    Example: receipt_line("Pen", 3, 1.5) -> "Pen            3      1.50"
    """
    pass


def format_percent(value: float, decimals: int) -> str:
    """
    Return `value` (a fraction, e.g. 0.256) as a percentage
    string with `decimals` digits after the decimal point and a
    trailing "%". The number of decimals must come from the
    `decimals` variable inside the format specification.

    Example: format_percent(0.256, 1) -> "25.6%"
    """
    pass


def format_binary(n: int, width: int) -> str:
    """
    Return `n` written in binary, zero-padded on the left to at
    least `width` digits. `n` is non-negative.
    Example: format_binary(5, 8) -> "00000101"
    """
    pass


def debug_label(label: str, value) -> str:
    """
    Return a string of the form label=<repr of value>. Use the
    !r conversion.
    Example: debug_label("name", "Ada") -> "name='Ada'"
             debug_label("n", 5)        -> "n=5"
    """
    pass
