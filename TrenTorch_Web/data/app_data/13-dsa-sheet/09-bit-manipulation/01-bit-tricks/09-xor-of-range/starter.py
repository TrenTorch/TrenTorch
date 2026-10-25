def xor_of_range(left: int, right: int) -> int:
    """Return left ^ (left + 1) ^ ... ^ right."""
    # This is correct but too slow: it xors the numbers one by one.
    result = 0
    for value in range(left, right + 1):
        result ^= value
    return result
