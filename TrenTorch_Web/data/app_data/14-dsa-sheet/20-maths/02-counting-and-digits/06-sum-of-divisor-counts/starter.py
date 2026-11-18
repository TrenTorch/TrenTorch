def sum_divisor_counts(n: int) -> int:
    """Return d(1) + d(2) + ... + d(n), where d(k) is the number of divisors of k."""
    # This is correct but too slow: it counts the multiples of every number up to n, one number at a time.
    return sum(n // k for k in range(1, n + 1))
