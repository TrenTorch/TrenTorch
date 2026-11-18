from functools import lru_cache


def can_jump(nums):
    n = len(nums)
    if n == 0:
        return True

    @lru_cache(maxsize=None)
    def reach(i):
        if i == n - 1:
            return True
        return any(reach(j) for j in range(i + 1, min(n, i + nums[i] + 1)))

    return reach(0)
