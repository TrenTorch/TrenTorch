def stock_best_profit(prices):
    """Return the biggest profit from one buy followed by one later sell."""
    # This is correct but too slow: it tries every pair of days.
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best
