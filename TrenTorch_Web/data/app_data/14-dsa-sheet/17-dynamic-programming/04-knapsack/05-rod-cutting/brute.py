def rod_cutting(prices, length):
    def go(n):
        if n == 0:
            return 0
        return max(prices[k - 1] + go(n - k) for k in range(1, n + 1))

    return go(length)
