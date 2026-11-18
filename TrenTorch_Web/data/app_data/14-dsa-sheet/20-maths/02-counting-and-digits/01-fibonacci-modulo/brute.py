def fib_mod(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % (10**9 + 7)
    return a
