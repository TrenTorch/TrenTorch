def count_primes(n: int) -> int:
    """Return how many prime numbers are smaller than n."""
    # This is correct but too slow: it tests every number by trial division.
    count = 0
    for x in range(2, n):
        if all(x % d for d in range(2, int(x**0.5) + 1)):
            count += 1
    return count
