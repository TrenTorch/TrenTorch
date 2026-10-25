def nth_fibonacci(n):
    if n < 2:
        return n
    return nth_fibonacci(n - 1) + nth_fibonacci(n - 2)
