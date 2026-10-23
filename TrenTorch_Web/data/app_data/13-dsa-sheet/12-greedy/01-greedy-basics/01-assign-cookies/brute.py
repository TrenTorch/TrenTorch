from functools import lru_cache


def assign_cookies(greed, sizes):
    @lru_cache(maxsize=None)
    def best(i, used):
        if i == len(greed):
            return 0
        result = best(i + 1, used)
        for j in range(len(sizes)):
            if not used >> j & 1 and sizes[j] >= greed[i]:
                result = max(result, 1 + best(i + 1, used | 1 << j))
        return result

    return best(0, 0)
