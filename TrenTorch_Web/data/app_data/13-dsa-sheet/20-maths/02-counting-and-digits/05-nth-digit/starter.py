def nth_digit(n: int) -> int:
    """Return the nth digit of the sequence 123456789101112..."""
    # This is correct but too slow: it writes the numbers one after another until the text is long enough.
    text = []
    length = 0
    k = 1
    while length < n:
        text.append(str(k))
        length += len(text[-1])
        k += 1
    return int("".join(text)[n - 1])
