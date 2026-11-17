def and_of_range(left: int, right: int) -> int:
    """Return left & (left + 1) & ... & right."""
    # This is correct but too slow: it ands the numbers one by one.
    result = left
    for value in range(left + 1, right + 1):
        result &= value
    return result
