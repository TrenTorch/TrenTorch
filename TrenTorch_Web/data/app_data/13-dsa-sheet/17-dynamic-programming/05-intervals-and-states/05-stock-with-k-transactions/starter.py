def max_profit_k(k: int, prices: list[int]) -> int:
    """Return the maximum profit using at most k buy-sell pairs."""

    # This is correct but too slow: it tries every action on every day without remembering results.
    def go(day, holding, left):
        if day == len(prices) or left == 0:
            return 0
        best = go(day + 1, holding, left)
        if holding:
            best = max(best, prices[day] + go(day + 1, False, left - 1))
        else:
            best = max(best, -prices[day] + go(day + 1, True, left))
        return best

    return go(0, False, k)
