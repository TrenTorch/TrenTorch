def stock_best_profit(prices):
    best = 0
    lowest = None
    for price in prices:
        if lowest is not None:
            best = max(best, price - lowest)
            lowest = min(lowest, price)
        else:
            lowest = price
    return best
