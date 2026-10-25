def count_divisors(n):
    return sum(1 for d in range(1, n + 1) if n % d == 0)
