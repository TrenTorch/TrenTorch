def trailing_zeros(n: int) -> int:
    """Return the number of zeros at the end of n!."""
    # This is correct but too slow: it visits every number up to n.
    count = 0
    for k in range(1, n + 1):
        while k % 5 == 0:
            k //= 5
            count += 1
    return count
