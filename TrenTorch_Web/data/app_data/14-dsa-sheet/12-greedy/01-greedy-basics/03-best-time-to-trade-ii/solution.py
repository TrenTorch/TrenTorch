def max_profit_many(prices):
    return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))
