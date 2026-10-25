from functools import lru_cache


def max_coins(nums):
    @lru_cache(maxsize=None)
    def go(items):
        if not items:
            return 0
        best = 0
        for i in range(len(items)):
            left = items[i - 1] if i > 0 else 1
            right = items[i + 1] if i + 1 < len(items) else 1
            best = max(best, left * items[i] * right + go(items[:i] + items[i + 1 :]))
        return best

    return go(tuple(nums))
