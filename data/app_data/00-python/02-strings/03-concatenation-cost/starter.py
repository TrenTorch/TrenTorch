def join_with_separator(parts, sep: str) -> str:
    """
    `parts` is a list of strings. Build and return one string
    containing every element of `parts`, with `sep` placed
    between consecutive elements (not before the first, not
    after the last). Use a for loop with + / += only. Do not
    use the join() method.

    An empty `parts` returns "".
    Example: join_with_separator(["a", "b", "c"], "-") -> "a-b-c"
    """
    pass


def repeat_text(s: str, n: int) -> str:
    """
    Return `s` repeated `n` times using the * operator.
    If n <= 0, return "".
    """
    pass


def total_chars_copied(n: int, piece_length: int) -> int:
    """
    Model of repeated concatenation. A string starts empty.
    For each of `n` steps, one piece of length `piece_length`
    is appended, and the step writes every character of the
    NEW string (previous content plus the piece).

    Return the total number of characters written across all
    n steps: piece_length * (1 + 2 + ... + n).
    If n <= 0, return 0.

    Example: total_chars_copied(3, 2) -> 2 + 4 + 6 = 12
    """
    pass
