def nth_fibonacci(n):
    """Return F(n), with F(0) = 0 and F(1) = 1."""
    # This is correct but far too slow: it recomputes the same values again and again.
    if n < 2:
        return n
    return nth_fibonacci(n - 1) + nth_fibonacci(n - 2)
