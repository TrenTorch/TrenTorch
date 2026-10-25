def max_profit_many(prices):
    n = len(prices)
    hold, free = float("-inf"), 0
    for p in prices:
        hold, free = max(hold, free - p), max(free, hold + p)
    return free if n else 0
