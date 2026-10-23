def num_squares(n):
    best = list(range(n + 1))
    for i in range(2, n + 1):
        k = 1
        while k * k <= i:
            if best[i - k * k] + 1 < best[i]:
                best[i] = best[i - k * k] + 1
            k += 1
    return best[n]
