from functools import lru_cache


def max_profit_k(k, prices):
    @lru_cache(maxsize=None)
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
