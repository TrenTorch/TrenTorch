def josephus(n, k):
    position = 0
    for m in range(2, n + 1):
        position = (position + k) % m
    return position + 1
