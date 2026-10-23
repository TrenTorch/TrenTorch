def num_squares(n: int) -> int:
    """Return the fewest perfect squares that add up to n."""
    # This is correct but too slow: it solves the same smaller numbers again and again.
    if n == 0:
        return 0
    best = n
    k = 1
    while k * k <= n:
        best = min(best, 1 + num_squares(n - k * k))
        k += 1
    return best
