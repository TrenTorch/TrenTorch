def binomial_mod(n, k):
    mod = 10**9 + 7
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    num = den = 1
    for i in range(k):
        num = num * ((n - i) % mod) % mod
        den = den * (i + 1) % mod
    return num * pow(den, mod - 2, mod) % mod
