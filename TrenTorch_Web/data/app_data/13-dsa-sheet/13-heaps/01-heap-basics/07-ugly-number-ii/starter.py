def nth_ugly_number(n: int) -> int:
    """Return the nth number whose only prime factors are 2, 3 and 5."""
    # This is correct but too slow: it tests the whole numbers 1, 2, 3, ... one by one.
    count = 0
    x = 0
    while count < n:
        x += 1
        y = x
        for p in (2, 3, 5):
            while y % p == 0:
                y //= p
        if y == 1:
            count += 1
    return x
