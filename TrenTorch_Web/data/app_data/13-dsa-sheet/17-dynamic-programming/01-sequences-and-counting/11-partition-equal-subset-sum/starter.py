def can_partition(nums: list[int]) -> bool:
    """Return True if the numbers can be split into two groups with equal sums."""
    # This is correct but too slow: it tries to include or skip every number without remembering results.
    total = sum(nums)
    if total % 2:
        return False
    half = total // 2

    def go(i, rest):
        if rest == 0:
            return True
        if i == len(nums) or rest < 0:
            return False
        return go(i + 1, rest - nums[i]) or go(i + 1, rest)

    return go(0, half)
