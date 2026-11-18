def count_divisors(n: int) -> int:
    """Return how many positive numbers divide n."""
    # This is correct but too slow: it tests every number up to n.
    return sum(1 for d in range(1, n + 1) if n % d == 0)
