def fib_mod(n):
    mod = 10**9 + 7

    def pair(k):
        if k == 0:
            return 0, 1
        a, b = pair(k // 2)
        c = a * ((2 * b - a) % mod) % mod
        e = (a * a + b * b) % mod
        return (e, (c + e) % mod) if k % 2 else (c, e)

    return pair(n)[0]
