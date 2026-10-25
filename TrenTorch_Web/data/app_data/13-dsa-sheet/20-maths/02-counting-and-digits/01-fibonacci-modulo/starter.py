def fib_mod(n: int) -> int:
    """Return the nth Fibonacci number modulo 10**9 + 7."""
    # This is correct but too slow: it adds up one number at a time.
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % (10**9 + 7)
    return a
