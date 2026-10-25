def is_prime(n: int) -> bool:
    """Return True if n is prime."""
    # This is correct but too slow for big primes: it tries every divisor up to the square root.
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True
