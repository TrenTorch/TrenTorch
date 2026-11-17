def binomial_mod(n: int, k: int) -> int:
    """Return C(n, k) modulo 10**9 + 7."""
    # This is correct but too slow: it builds the exact (huge) number first.
    if k < 0:
        return 0
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result % (10**9 + 7)
