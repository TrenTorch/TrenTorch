def climb_stairs(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, (a + b) % (10**9 + 7)
    return a
