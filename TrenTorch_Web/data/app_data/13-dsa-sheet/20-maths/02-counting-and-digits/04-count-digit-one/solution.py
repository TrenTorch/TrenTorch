def count_digit_one(n):
    total = 0
    p = 1
    while p <= n:
        high = n // (p * 10)
        cur = (n // p) % 10
        low = n % p
        total += high * p
        if cur > 1:
            total += p
        elif cur == 1:
            total += low + 1
        p *= 10
    return total
