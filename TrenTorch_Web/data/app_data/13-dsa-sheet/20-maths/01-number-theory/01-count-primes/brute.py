def count_primes(n):
    return sum(1 for x in range(2, n) if all(x % d for d in range(2, x)))
