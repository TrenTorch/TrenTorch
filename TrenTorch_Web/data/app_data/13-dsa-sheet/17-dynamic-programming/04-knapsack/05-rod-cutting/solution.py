def rod_cutting(prices, length):
    best = [0] * (length + 1)
    for n in range(1, length + 1):
        for k in range(1, n + 1):
            if prices[k - 1] + best[n - k] > best[n]:
                best[n] = prices[k - 1] + best[n - k]
    return best[length]
