def max_profit_cooldown(prices: list[int]) -> int:
    """Return the maximum profit when you must wait one day after selling."""

    # This is correct but too slow: it tries every action on every day without remembering results.
    def go(day, holding):
        if day >= len(prices):
            return 0
        best = go(day + 1, holding)
        if holding:
            best = max(best, prices[day] + go(day + 2, False))
        else:
            best = max(best, -prices[day] + go(day + 1, True))
        return best

    return go(0, False)
