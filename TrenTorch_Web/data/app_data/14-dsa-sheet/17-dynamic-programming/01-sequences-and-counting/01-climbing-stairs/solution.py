MOD = 10**9 + 7


def climb_stairs(n):
    def fib(k):
        # returns (F(k), F(k + 1)) modulo MOD
        if k == 0:
            return 0, 1
        a, b = fib(k >> 1)
        c = a * (2 * b - a) % MOD
        d = (a * a + b * b) % MOD
        return (d, (c + d) % MOD) if k & 1 else (c, d)

    return fib(n + 1)[0]
