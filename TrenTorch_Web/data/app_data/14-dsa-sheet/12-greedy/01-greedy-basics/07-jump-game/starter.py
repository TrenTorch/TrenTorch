def can_jump(nums: list[int]) -> bool:
    """Return True if you can reach the last index."""
    # This is correct but too slow: for every position it checks every position that can still reach the end.
    n = len(nums)
    if n == 0:
        return True
    good = [False] * n
    good[n - 1] = True
    for i in range(n - 2, -1, -1):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if good[j]:
                good[i] = True
                break
    return good[0]
