def max_profit_k(k, prices):
    if k == 0 or len(prices) < 2:
        return 0
    if k >= len(prices) // 2:
        return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))
    hold = [float("-inf")] * (k + 1)
    free = [0] * (k + 1)
    for p in prices:
        for t in range(1, k + 1):
            hold[t] = max(hold[t], free[t - 1] - p)
            free[t] = max(free[t], hold[t] + p)
    return free[k]
