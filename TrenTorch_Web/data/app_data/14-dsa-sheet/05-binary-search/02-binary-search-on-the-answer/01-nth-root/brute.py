def nth_root(n, m):
    x = 1
    while True:
        power = x**m
        if power == n:
            return x
        if power > n:
            return -1
        x += 1
