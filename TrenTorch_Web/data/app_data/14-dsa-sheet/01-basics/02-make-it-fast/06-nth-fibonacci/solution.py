def nth_fibonacci(n):
    def fib(k):
        # returns (F(k), F(k + 1))
        if k == 0:
            return 0, 1
        a, b = fib(k >> 1)
        c = a * (2 * b - a)
        d = a * a + b * b
        return (d, c + d) if k & 1 else (c, d)

    return fib(n)[0]
