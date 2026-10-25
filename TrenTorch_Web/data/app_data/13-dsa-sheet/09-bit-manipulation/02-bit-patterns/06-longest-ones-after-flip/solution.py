def longest_ones_after_flip(n):
    best = current = previous = 0
    for i in range(32):
        if (n >> i) & 1:
            current += 1
        else:
            previous = current
            current = 0
        best = max(best, previous + current + 1)
    return min(best, 32)
