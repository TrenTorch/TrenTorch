from functools import lru_cache


def max_profit_cooldown(prices):
    @lru_cache(maxsize=None)
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
