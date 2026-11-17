from functools import lru_cache


def egg_drop(eggs, floors):
    if floors == 0 or eggs == 0:
        return 0

    @lru_cache(maxsize=None)
    def go(e, f):
        if f == 0:
            return 0
        if e == 1:
            return f
        return 1 + min(max(go(e - 1, x - 1), go(e, f - x)) for x in range(1, f + 1))

    return go(eggs, floors)
