def prime_factors(n):
    out = []
    for d in range(2, n + 1):
        if n % d == 0 and all(d % k for k in range(2, d)):
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            out.append([d, e])
    return out
