def count_digit_one(n: int) -> int:
    """Return how many times the digit 1 appears in all numbers from 1 to n."""
    # This is correct but too slow: it looks at the digits of every number up to n.
    return sum(str(k).count("1") for k in range(1, n + 1))
